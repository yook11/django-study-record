import { Pagination } from "./Pagination";
import type { components } from "../api/schema";

type ItemSchema = components["schemas"]["ItemSchema"];

interface ItemListProps {
  items: ItemSchema[];
  totalCount: number;
  currentPage: number;
  itemsPerPage: number;
  isLoading: boolean;
  error: Error | null;
  onDelete: (id: number) => void;
  onPageChange: (page: number) => void;
}

export const ItemList = ({
  items,
  totalCount,
  currentPage,
  itemsPerPage,
  isLoading,
  error,
  onDelete,
  onPageChange
}: ItemListProps) => {
  // ローディング・エラー表示
  if (isLoading) return <p>読み込み中...</p>;
  if (error) return <p>エラーが発生しました: {error.message}</p>;

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "0 auto" }}>
      <h2>📦 商品一覧</h2>

      {totalCount === 0 ? (
        <p>商品がまだありません。</p>
      ) : (
        <>
          <ul style={{ listStyle: "none", padding: 0 }}>
            {items.map((item) => (
              <li
                key={item.id}
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
                <div>
                  <span style={{ fontWeight: "bold", fontSize: "1.1rem" }}>
                    {item.name}
                  </span>
                  <span style={{ marginLeft: "10px", color: "#666" }}>
                    ¥{item.price}
                  </span>
                </div>

                <button
                  onClick={() => {
                    if (window.confirm(`「${item.name}」を削除しますか？`)) {
                      onDelete(item.id);
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

          {/* ページネーションUI */}
          <Pagination
            currentPage={currentPage}
            totalCount={totalCount}
            itemsPerPage={itemsPerPage}
            onPageChange={onPageChange}
          />
        </>
      )}
    </div>
  );
};
