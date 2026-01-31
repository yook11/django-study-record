// ページの読み込みが完了したら以下の処理を実行
document.addEventListener('DOMContentLoaded', function() {
    // すべてのメッセージ要素（クラス名が "message"）を取得
    var messages = document.querySelectorAll('.message');

    // 各メッセージに対して処理を実行
    messages.forEach(function(message) {
        // 5秒後にメッセージをフェードアウトして消す
        setTimeout(function() {
            // フェードアウト用のクラスを追加（これでCSSが反応して透明になる）
            message.classList.add('fade-out');
            
            // フェードアウトのアニメーション完了後（0.5秒後）に要素を完全に削除
            setTimeout(function() {
                message.remove();
            }, 500); // 0.5秒後
        }, 5000); // 5秒後

        // メッセージにある閉じるボタン（クラス名が "close-btn"）のクリックイベントを設定
        var closeBtn = message.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                // ボタンがクリックされたらメッセージをフェードアウト
                message.classList.add('fade-out');
                setTimeout(function() {
                    message.remove();
                }, 500); // 0.5秒後
            });
        }
    });
});