// Pixel Realm RPG - C++/SDL2 rewrite
// PHASE 1: chung minh toolchain build+chay tren Android.
// Co: di chuyen bang nut cham, tan cong (attack), ne (dodge), hoat anh trung don co ban.
// Chua co: mob, shop, tien te, big map + culling, nhieu quoc gia -> se them o cac pha sau.
//
// Kien truc de mo rong:
//   - Entity: player, sau nay them Mob voi cung struct
//   - Button: nut cham UI, ve bang hinh chu nhat (placeholder cho PNG that sau nay)
//   - Camera: hien tai co dinh, pha sau se theo player + chi render vung trong man hinh

#include <SDL.h>
#include <cmath>
#include <cstdio>
#include <vector>

static const int SCREEN_W = 960;
static const int SCREEN_H = 540;
static const float PLAYER_SPEED = 220.0f; // pixel/giay
static const float DODGE_SPEED = 700.0f;
static const float DODGE_DURATION = 0.18f;
static const float DODGE_COOLDOWN = 0.6f;
static const float ATTACK_DURATION = 0.22f;
static const float ATTACK_COOLDOWN = 0.35f;
static const float HURT_FLASH_DURATION = 0.4f;

struct Button {
    SDL_Rect rect;
    SDL_Color color;
    SDL_Color pressedColor;
    bool pressed = false;
    SDL_FingerID fingerId = -1;
    bool fingerActive = false;

    bool contains(int x, int y) const {
        return x >= rect.x && x < rect.x + rect.w &&
               y >= rect.y && y < rect.y + rect.h;
    }
};

struct Player {
    float x = SCREEN_W / 2.0f;
    float y = SCREEN_H / 2.0f;
    float dirX = 0.0f, dirY = -1.0f; // huong nhin gan nhat, dung cho ve don chem
    int size = 36;

    bool isDodging = false;
    float dodgeTimer = 0.0f;
    float dodgeCooldown = 0.0f;
    float dodgeDirX = 0.0f, dodgeDirY = 0.0f;

    bool isAttacking = false;
    float attackTimer = 0.0f;
    float attackCooldown = 0.0f;

    float hurtFlashTimer = 0.0f; // >0 nghia la dang nhap nhay do (vua trung don)

    bool isInvulnerable() const { return isDodging; }
};

static void triggerAttack(Player &p) {
    if (p.attackCooldown > 0.0f || p.isDodging) return;
    p.isAttacking = true;
    p.attackTimer = ATTACK_DURATION;
    p.attackCooldown = ATTACK_COOLDOWN;
}

static void triggerDodge(Player &p, float moveX, float moveY) {
    if (p.dodgeCooldown > 0.0f || p.isDodging) return;
    float len = std::sqrt(moveX * moveX + moveY * moveY);
    if (len < 0.01f) {
        // dung yen thi ne theo huong dang nhin
        p.dodgeDirX = p.dirX;
        p.dodgeDirY = p.dirY;
    } else {
        p.dodgeDirX = moveX / len;
        p.dodgeDirY = moveY / len;
    }
    p.isDodging = true;
    p.dodgeTimer = DODGE_DURATION;
    p.dodgeCooldown = DODGE_COOLDOWN;
}

// Giu lai de test co che nhan damage; sau nay Mob se goi ham nay khi va cham Player.
static void takeHit(Player &p) {
    if (p.isInvulnerable()) return; // dang ne thi mien nhiem
    p.hurtFlashTimer = HURT_FLASH_DURATION;
}

int main(int argc, char *argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "SDL_Init lỗi: %s", SDL_GetError());
        return 1;
    }

    SDL_Window *window = SDL_CreateWindow(
        "Pixel Realm RPG",
        SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
        SCREEN_W, SCREEN_H,
        SDL_WINDOW_SHOWN | SDL_WINDOW_FULLSCREEN_DESKTOP | SDL_WINDOW_RESIZABLE);
    if (!window) {
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "CreateWindow lỗi: %s", SDL_GetError());
        return 1;
    }

    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (!renderer) {
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "CreateRenderer lỗi: %s", SDL_GetError());
        return 1;
    }

    // Lấy kích thước thực tế của màn hình (Android thường fullscreen khác 960x540)
    int actualW, actualH;
    SDL_GetRendererOutputSize(renderer, &actualW, &actualH);
    SDL_RenderSetLogicalSize(renderer, SCREEN_W, SCREEN_H); // giữ toạ độ game cố định 960x540, SDL tự scale

    Player player;

    // --- Nut dieu khien (placeholder hinh chu nhat, sau nay thay bang PNG icon) ---
    int btnSize = 64;
    int pad = 12;
    Button btnUp{{pad + btnSize, SCREEN_H - pad - btnSize * 3, btnSize, btnSize}, {70, 70, 90, 180}, {120, 120, 160, 220}};
    Button btnDown{{pad + btnSize, SCREEN_H - pad - btnSize, btnSize, btnSize}, {70, 70, 90, 180}, {120, 120, 160, 220}};
    Button btnLeft{{pad, SCREEN_H - pad - btnSize * 2, btnSize, btnSize}, {70, 70, 90, 180}, {120, 120, 160, 220}};
    Button btnRight{{pad + btnSize * 2, SCREEN_H - pad - btnSize * 2, btnSize, btnSize}, {70, 70, 90, 180}, {120, 120, 160, 220}};
    Button btnAttack{{SCREEN_W - pad - btnSize, SCREEN_H - pad - btnSize * 2 - 10, btnSize, btnSize}, {170, 60, 60, 200}, {220, 90, 90, 240}};
    Button btnDodge{{SCREEN_W - pad - btnSize * 2 - 10, SCREEN_H - pad - btnSize, btnSize, btnSize}, {60, 130, 170, 200}, {90, 170, 220, 240}};

    std::vector<Button *> dirButtons = {&btnUp, &btnDown, &btnLeft, &btnRight};

    Uint64 lastCounter = SDL_GetPerformanceCounter();
    bool running = true;

    while (running) {
        Uint64 nowCounter = SDL_GetPerformanceCounter();
        float dt = (float)(nowCounter - lastCounter) / (float)SDL_GetPerformanceFrequency();
        lastCounter = nowCounter;
        if (dt > 0.05f) dt = 0.05f; // tránh bước nhảy lớn khi app bị pause/resume

        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_QUIT) running = false;

            // Android/di dong: SDL bắn ca finger event lan mouse event (tu dong dich tu touch).
            // Dung finger event de ho tro da cham (multi-touch) cho di chuyen + tan cong cung luc.
            if (e.type == SDL_FINGERDOWN || e.type == SDL_FINGERUP) {
                int px = (int)(e.tfinger.x * actualW);
                int py = (int)(e.tfinger.y * actualH);
                // quy doi tu toa do man hinh thuc te ve toa do logic 960x540
                float scaleX = (float)SCREEN_W / (float)actualW;
                float scaleY = (float)SCREEN_H / (float)actualH;
                int lx = (int)(px * scaleX);
                int ly = (int)(py * scaleY);

                for (Button *b : dirButtons) {
                    if (e.type == SDL_FINGERDOWN && b->contains(lx, ly) && !b->fingerActive) {
                        b->fingerActive = true;
                        b->fingerId = e.tfinger.fingerId;
                        b->pressed = true;
                    } else if (e.type == SDL_FINGERUP && b->fingerActive && b->fingerId == e.tfinger.fingerId) {
                        b->fingerActive = false;
                        b->pressed = false;
                    }
                }
                if (e.type == SDL_FINGERDOWN && btnAttack.contains(lx, ly)) {
                    triggerAttack(player);
                }
                if (e.type == SDL_FINGERDOWN && btnDodge.contains(lx, ly)) {
                    float mx = (btnRight.pressed ? 1.f : 0.f) - (btnLeft.pressed ? 1.f : 0.f);
                    float my = (btnDown.pressed ? 1.f : 0.f) - (btnUp.pressed ? 1.f : 0.f);
                    triggerDodge(player, mx, my);
                }
            }

            // Fallback: chuot/ban phim de test tren desktop (Termux khong co, nhung tien test local)
            if (e.type == SDL_KEYDOWN) {
                if (e.key.keysym.sym == SDLK_ESCAPE) running = false;
                if (e.key.keysym.sym == SDLK_SPACE) triggerAttack(player);
                if (e.key.keysym.sym == SDLK_LSHIFT) {
                    float mx = (btnRight.pressed ? 1.f : 0.f) - (btnLeft.pressed ? 1.f : 0.f);
                    float my = (btnDown.pressed ? 1.f : 0.f) - (btnUp.pressed ? 1.f : 0.f);
                    triggerDodge(player, mx, my);
                }
            }
        }

        // --- ban phim desktop fallback cho 4 huong (khong anh huong Android) ---
        const Uint8 *keys = SDL_GetKeyboardState(nullptr);
        bool kUp = keys[SDL_SCANCODE_UP] || keys[SDL_SCANCODE_W];
        bool kDown = keys[SDL_SCANCODE_DOWN] || keys[SDL_SCANCODE_S];
        bool kLeft = keys[SDL_SCANCODE_LEFT] || keys[SDL_SCANCODE_A];
        bool kRight = keys[SDL_SCANCODE_RIGHT] || keys[SDL_SCANCODE_D];

        float moveX = (btnRight.pressed || kRight ? 1.f : 0.f) - (btnLeft.pressed || kLeft ? 1.f : 0.f);
        float moveY = (btnDown.pressed || kDown ? 1.f : 0.f) - (btnUp.pressed || kUp ? 1.f : 0.f);

        // --- cap nhat timer ---
        if (player.attackCooldown > 0.0f) player.attackCooldown -= dt;
        if (player.dodgeCooldown > 0.0f) player.dodgeCooldown -= dt;
        if (player.hurtFlashTimer > 0.0f) player.hurtFlashTimer -= dt;

        if (player.isAttacking) {
            player.attackTimer -= dt;
            if (player.attackTimer <= 0.0f) player.isAttacking = false;
        }

        if (player.isDodging) {
            player.dodgeTimer -= dt;
            player.x += player.dodgeDirX * DODGE_SPEED * dt;
            player.y += player.dodgeDirY * DODGE_SPEED * dt;
            if (player.dodgeTimer <= 0.0f) player.isDodging = false;
        } else {
            float len = std::sqrt(moveX * moveX + moveY * moveY);
            if (len > 0.01f) {
                float nx = moveX / len, ny = moveY / len;
                player.x += nx * PLAYER_SPEED * dt;
                player.y += ny * PLAYER_SPEED * dt;
                player.dirX = nx;
                player.dirY = ny;
            }
        }

        // gioi han trong man hinh (tam thoi, sau nay thay bang collision voi map)
        if (player.x < player.size / 2.f) player.x = player.size / 2.f;
        if (player.x > SCREEN_W - player.size / 2.f) player.x = SCREEN_W - player.size / 2.f;
        if (player.y < player.size / 2.f) player.y = player.size / 2.f;
        if (player.y > SCREEN_H - player.size / 2.f) player.y = SCREEN_H - player.size / 2.f;

        // --- render ---
        SDL_SetRenderDrawColor(renderer, 24, 26, 32, 255);
        SDL_RenderClear(renderer);

        // luoi nen tam thoi (placeholder cho tilemap that)
        SDL_SetRenderDrawColor(renderer, 36, 40, 48, 255);
        for (int gx = 0; gx < SCREEN_W; gx += 48) SDL_RenderDrawLine(renderer, gx, 0, gx, SCREEN_H);
        for (int gy = 0; gy < SCREEN_H; gy += 48) SDL_RenderDrawLine(renderer, 0, gy, SCREEN_W, gy);

        // player: nhap nhay do neu vua trung don, mo neu dang ne
        SDL_Rect playerRect{(int)(player.x - player.size / 2), (int)(player.y - player.size / 2), player.size, player.size};
        if (player.hurtFlashTimer > 0.0f && ((int)(player.hurtFlashTimer * 20) % 2 == 0)) {
            SDL_SetRenderDrawColor(renderer, 230, 60, 60, 255);
        } else if (player.isDodging) {
            SDL_SetRenderDrawColor(renderer, 230, 190, 120, 120);
        } else {
            SDL_SetRenderDrawColor(renderer, 230, 190, 120, 255);
        }
        SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);
        SDL_RenderFillRect(renderer, &playerRect);

        // ve don chem placeholder: hinh cung mau trang mo huong player dang nhin
        if (player.isAttacking) {
            float swingProgress = 1.0f - (player.attackTimer / ATTACK_DURATION);
            float reach = 44.0f + swingProgress * 10.0f;
            SDL_Rect slash{
                (int)(player.x + player.dirX * reach - 20),
                (int)(player.y + player.dirY * reach - 20),
                40, 40};
            SDL_SetRenderDrawColor(renderer, 255, 255, 255, (Uint8)(200 * (1.0f - swingProgress)));
            SDL_RenderFillRect(renderer, &slash);
        }

        // ve nut dieu khien
        for (Button *b : dirButtons) {
            SDL_Color c = b->pressed ? b->pressedColor : b->color;
            SDL_SetRenderDrawColor(renderer, c.r, c.g, c.b, c.a);
            SDL_RenderFillRect(renderer, &b->rect);
        }
        {
            SDL_Color c = (player.attackCooldown > 0.0f) ? SDL_Color{100, 40, 40, 160} : btnAttack.color;
            SDL_SetRenderDrawColor(renderer, c.r, c.g, c.b, c.a);
            SDL_RenderFillRect(renderer, &btnAttack.rect);

            c = (player.dodgeCooldown > 0.0f) ? SDL_Color{40, 80, 100, 160} : btnDodge.color;
            SDL_SetRenderDrawColor(renderer, c.r, c.g, c.b, c.a);
            SDL_RenderFillRect(renderer, &btnDodge.rect);
        }

        SDL_RenderPresent(renderer);
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
