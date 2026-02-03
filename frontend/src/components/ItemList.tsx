import { useGetItems, useDeleteItem } from "../api/hooks";


export const ItemList = () => {
  // 1. 読み込み係（ウェイター）を呼ぶ
  // data: 取得したリスト, isLoading: 読み込み中か？, error: エラーか？
  const { data: items, isLoading, error } = useGetItems();

  // 2. 削除係（掃除屋）を呼ぶ
  const deleteMutation = useDeleteItem();

  // 3. 状態に応じた表示（条件分岐）
  if (isLoading) return <p>読み込み中...</p>;
  if (error) return <p>エラーが発生しました: {error.message}</p>;

  // 4. メインの表示（データがある場合）
  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "0 auto" }}>
      <h2>📦 商品一覧</h2>
      
      {/* リストが空の場合の表示 */}
      {items?.length === 0 && <p>商品がまだありません。</p>}

      {/* mapを使って、データの数だけ <div> を繰り返し作成 */}
      <ul style={{ listStyle: "none", padding: 0 }}>
        {items?.map((item) => (
          <li
            key={item.id} // ⚠️ Reactのループには必ず一意なkeyが必要
            style={{
              border: "1px solid #ddd",
              borderRadius: "8px",
              padding: "16px",
              marginBottom: "12px",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              backgroundColor: "#fff",
              boxShadow: "0 2px 4px rgba(0,0,0,0.05)"
            }}
          >
            {/* 左側：商品情報 */}
            <div>
              <span style={{ fontWeight: "bold", fontSize: "1.1rem" }}>
                {item.name}
              </span>
              <span style={{ marginLeft: "10px", color: "#666" }}>
                ¥{item.price}
              </span>
            </div>

            {/* 右側：削除ボタン */}
            <button
              onClick={() => {
                if (window.confirm(`「${item.name}」を削除しますか？`)) {
                  deleteMutation.mutate(item.id);
                }
              }}
              style={{
                backgroundColor: "#ff4d4f",
                color: "white",
                border: "none",
                borderRadius: "4px",
                padding: "8px 12px",
                cursor: "pointer",
              }}
            >
              削除
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};