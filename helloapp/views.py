# HttpResponseクラスをインポート
from django.http import HttpResponse


# ------------------------------------------------------------------
# ビュー関数を定義
# "ハロー、Django!"というテキストを含むHTTPレスポンスを返す
# ------------------------------------------------------------------
def show_hello(request):
    # ▽▽▽▽▽ 7.6 ▽▽▽▽▽
    html_content = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hello Django - 書道</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Yuji+Syuku&family=Zen+Antique&display=swap" rel="stylesheet"> # noqa: E501
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                background: linear-gradient(to bottom, #f5f5dc 0%, #e8e3d3 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                overflow: hidden;
            }

            body::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: 
                    radial-gradient(circle at 20% 30%, rgba(139, 69, 19, 0.03) 0%, transparent 50%),
                    radial-gradient(circle at 80% 70%, rgba(139, 69, 19, 0.03) 0%, transparent 50%),
                    radial-gradient(circle at 40% 80%, rgba(139, 69, 19, 0.02) 0%, transparent 50%);
                pointer-events: none;
            }

            .canvas {
                position: relative;
                width: 90%;
                max-width: 1200px;
                background: rgba(255, 255, 255, 0.8);
                border: 20px solid #8b4513;
                border-image: linear-gradient(45deg, #654321, #8b4513, #a0522d) 1;
                box-shadow: 
                    0 30px 80px rgba(0, 0, 0, 0.3),
                    inset 0 0 100px rgba(139, 69, 19, 0.1);
                padding: 80px 40px;
                animation: fadeIn 1s ease-in;
            }

            .calligraphy {
                text-align: center;
                position: relative;
                animation: brushStroke 1.5s ease-out;
            }

            .main-text {
                font-family: 'Yuji Syuku', serif;
                font-size: clamp(4rem, 15vw, 12rem);
                color: #1a1a1a;
                line-height: 1.2;
                margin-bottom: 40px;
                text-shadow: 
                    3px 3px 0px rgba(0, 0, 0, 0.1),
                    6px 6px 0px rgba(0, 0, 0, 0.05);
                position: relative;
                display: inline-block;
                filter: 
                    contrast(1.2)
                    brightness(0.95);
            }

            .main-text::before {
                content: 'ハロー';
                position: absolute;
                top: 0;
                left: 0;
                color: rgba(139, 69, 19, 0.2);
                filter: blur(2px);
                transform: translate(2px, 2px);
                z-index: -1;
            }

            .django-text {
                font-family: 'Zen Antique', serif;
                font-size: clamp(3rem, 12vw, 10rem);
                background: linear-gradient(135deg, #1a1a1a 0%, #4a4a4a 50%, #1a1a1a 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                display: inline-block;
                position: relative;
                filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.3));
            }

            .brush-stroke {
                position: absolute;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                pointer-events: none;
                opacity: 0.1;
                background: 
                    radial-gradient(ellipse at 30% 40%, rgba(0,0,0,0.1) 0%, transparent 60%),
                    radial-gradient(ellipse at 70% 60%, rgba(0,0,0,0.1) 0%, transparent 60%);
            }

            .ink-splash {
                position: absolute;
                width: 150px;
                height: 150px;
                background: radial-gradient(circle, rgba(0,0,0,0.05) 0%, transparent 70%);
                border-radius: 50%;
                animation: splash 2s ease-in-out infinite;
            }

            .splash-1 {
                top: 10%;
                left: 15%;
                animation-delay: 0s;
            }

            .splash-2 {
                bottom: 15%;
                right: 20%;
                animation-delay: 0.7s;
            }

            .splash-3 {
                top: 60%;
                left: 70%;
                animation-delay: 1.4s;
            }

            .back-link {
                display: inline-block;
                margin-top: 50px;
                padding: 18px 50px;
                background: linear-gradient(135deg, #8b4513 0%, #654321 100%);
                color: #f5f5dc;
                text-decoration: none;
                border-radius: 50px;
                font-weight: 600;
                font-size: 1.1rem;
                transition: all 0.3s ease;
                box-shadow: 0 6px 20px rgba(139, 69, 19, 0.4);
                font-family: 'Zen Antique', serif;
                letter-spacing: 2px;
            }

            .back-link:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 30px rgba(139, 69, 19, 0.6);
                background: linear-gradient(135deg, #654321 0%, #8b4513 100%);
            }

            .seal {
                position: absolute;
                bottom: 40px;
                right: 40px;
                width: 80px;
                height: 80px;
                background: radial-gradient(circle, #dc143c 0%, #8b0000 100%);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 900;
                font-size: 1.5rem;
                box-shadow: 0 4px 15px rgba(220, 20, 60, 0.5);
                transform: rotate(-5deg);
                animation: stamp 0.5s ease-out 1.5s both;
            }

            @keyframes fadeIn {
                from {
                    opacity: 0;
                }
                to {
                    opacity: 1;
                }
            }

            @keyframes brushStroke {
                from {
                    opacity: 0;
                    filter: blur(10px);
                }
                to {
                    opacity: 1;
                    filter: blur(0px);
                }
            }

            @keyframes splash {
                0%, 100% {
                    transform: scale(1);
                    opacity: 0.05;
                }
                50% {
                    transform: scale(1.2);
                    opacity: 0.1;
                }
            }

            @keyframes stamp {
                0% {
                    opacity: 0;
                    transform: rotate(-5deg) scale(0);
                }
                50% {
                    transform: rotate(-5deg) scale(1.2);
                }
                100% {
                    opacity: 1;
                    transform: rotate(-5deg) scale(1);
                }
            }

            @media (max-width: 768px) {
                .canvas {
                    padding: 60px 30px;
                    border-width: 15px;
                }

                .main-text {
                    margin-bottom: 30px;
                }

                .seal {
                    width: 60px;
                    height: 60px;
                    font-size: 1.2rem;
                    bottom: 30px;
                    right: 30px;
                }
            }
        </style>
    </head>
    <body>
        <div class="ink-splash splash-1"></div>
        <div class="ink-splash splash-2"></div>
        <div class="ink-splash splash-3"></div>
        
        <div class="canvas">
            <div class="brush-stroke"></div>
            
            <div class="calligraphy">
                <div class="main-text">
                    ハロー
                </div>
                <div class="django-text">
                    Django！
                </div>
            </div>

            <a href="/menu/" class="back-link">
                ⛩️ メニューに戻る
            </a>

            <div class="seal">
                印
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)
    # △△△△△ 7.6 △△△△△
