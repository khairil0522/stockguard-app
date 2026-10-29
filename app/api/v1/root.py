from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/",response_class=HTMLResponse, include_in_schema=False)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="theme-color" content="#0b1120">
        <title>StockGuard | Inventory API</title>

        <style>
            :root {
                --bg: #0b1120;
                --panel: #111c2e;
                --border: #26354a;
                --text: #f1f5f9;
                --muted: #94a3b8;
                --green: #4ade80;
                --green-dark: #163b2b;
            }

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                background:
                    radial-gradient(
                        ellipse at 50% 0%,
                        #163126 0%,
                        var(--bg) 48%
                    );
                color: var(--text);
                font-family: Inter, -apple-system, BlinkMacSystemFont,
                    "Segoe UI", sans-serif;
            }

            nav {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 24px 8%;
                border-bottom: 1px solid rgba(148, 163, 184, 0.12);
            }

            .brand {
                display: flex;
                align-items: center;
                gap: 12px;
                font-size: 20px;
                font-weight: 750;
                letter-spacing: -0.6px;
            }

            .logo {
                display: grid;
                place-items: center;
                width: 38px;
                height: 38px;
                border-radius: 12px;
                background: var(--green-dark);
                color: var(--green);
                font-size: 22px;
            }

            .nav-label {
                color: var(--muted);
                font-size: 13px;
            }

            main {
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 72px 24px;
            }

            .hero {
                width: 100%;
                max-width: 760px;
                text-align: center;
            }

            .eyebrow {
                display: inline-flex;
                align-items: center;
                gap: 9px;
                padding: 9px 14px;
                margin-bottom: 28px;
                border: 1px solid #28543c;
                border-radius: 999px;
                background: rgba(22, 59, 43, 0.45);
                color: var(--green);
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 1.3px;
            }

            .dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: var(--green);
                box-shadow: 0 0 12px rgba(74, 222, 128, 0.65);
            }

            h1 {
                margin-bottom: 22px;
                font-size: clamp(42px, 7vw, 68px);
                line-height: 1.08;
                letter-spacing: -3px;
            }

            h1 span {
                color: var(--green);
            }

            .description {
                max-width: 560px;
                margin: 0 auto;
                color: var(--muted);
                font-size: 17px;
                line-height: 1.8;
            }

            .status-card {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 16px;
                max-width: 430px;
                margin: 36px auto;
                padding: 20px 22px;
                border: 1px solid var(--border);
                border-radius: 16px;
                background: rgba(17, 28, 46, 0.85);
                text-align: left;
            }

            .status-title {
                margin-bottom: 6px;
                font-size: 14px;
                font-weight: 650;
            }

            .status-subtitle {
                color: var(--muted);
                font-size: 12px;
            }

            .status-badge {
                display: inline-flex;
                align-items: center;
                gap: 7px;
                padding: 8px 11px;
                border-radius: 8px;
                background: var(--green-dark);
                color: var(--green);
                font-size: 12px;
                font-weight: 750;
                white-space: nowrap;
            }

            .actions {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
            }

            .button {
                display: inline-flex;
                justify-content: center;
                align-items: center;
                gap: 10px;
                min-height: 48px;
                padding: 0 22px;
                border: 1px solid transparent;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 700;
                text-decoration: none;
                transition: transform 0.2s, background 0.2s;
            }

            .button:hover {
                transform: translateY(-2px);
            }

            .button-primary {
                background: var(--green);
                color: #07140c;
            }

            .button-primary:hover {
                background: #86efac;
            }

            .button-secondary {
                border-color: var(--border);
                background: var(--panel);
                color: var(--text);
            }

            .button-secondary:hover {
                background: #1b2a40;
            }

            footer {
                padding: 24px;
                border-top: 1px solid rgba(148, 163, 184, 0.12);
                color: var(--muted);
                font-size: 12px;
                text-align: center;
            }

            footer span {
                color: var(--green);
            }

            @media (max-width: 480px) {
                nav {
                    padding: 18px 20px;
                }

                .nav-label {
                    font-size: 11px;
                }

                main {
                    padding: 56px 20px;
                }

                h1 {
                    letter-spacing: -2px;
                }

                .description {
                    font-size: 15px;
                }

                .status-card {
                    align-items: flex-start;
                    flex-direction: column;
                }

                .actions {
                    flex-direction: column;
                }

                .button {
                    width: 100%;
                }
            }
        </style>
    </head>

    <body>
        <nav>
            <div class="brand">
                <div class="logo">&#9632;</div>
                <span>StockGuard</span>
            </div>
            <div class="nav-label">INVENTORY MANAGEMENT API</div>
        </nav>

        <main>
            <section class="hero">
                <div class="eyebrow">
                    <span class="dot"></span>
                    INVENTORY API PLATFORM
                </div>

                <h1>
                    Inventory under<br>
                    <span>control.</span>
                </h1>

                <p class="description">
                    A reliable inventory and stock reservation API built
                    with FastAPI and PostgreSQL. Manage products, track stock
                    movements, and protect inventory consistency.
                </p>

                <div class="status-card">
                    <div>
                        <div class="status-title">API Service</div>
                        <div class="status-subtitle">
                            StockGuard backend service
                        </div>
                    </div>

                    <div class="status-badge">
                        <span class="dot"></span>
                        Operational
                    </div>
                </div>

                <div class="actions">
                    <a class="button button-primary" href="/docs">
                        Explore Swagger UI &#8599;
                    </a>

                    <a class="button button-secondary" href="/redoc">
                        Read API Reference &#8599;
                    </a>
                </div>
            </section>
        </main>

        <footer>
            Built with <span>FastAPI</span> &middot;
            Powered by PostgreSQL &middot; StockGuard API
            &middot; By Khairil Anwar
        </footer>
    </body>
    </html>
    """