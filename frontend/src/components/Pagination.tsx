interface PaginationProps {
  currentPage: number;       // 現在のページ番号（1始まり）
  totalCount: number;        // 全商品数
  itemsPerPage: number;      // 1ページあたりの件数
  onPageChange: (page: number) => void;  // ページ変更時のコールバック
}

export const Pagination = ({
  currentPage,
  totalCount,
  itemsPerPage,
  onPageChange
}: PaginationProps) => {
  const totalPages = Math.ceil(totalCount / itemsPerPage);
  const hasPrevious = currentPage > 1;
  const hasNext = currentPage < totalPages;

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      gap: '16px',
      marginTop: '20px'
    }}>
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={!hasPrevious}
        aria-label="前のページへ移動"
        style={{
          padding: '8px 16px',
          cursor: hasPrevious ? 'pointer' : 'not-allowed',
          opacity: hasPrevious ? 1 : 0.5,
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px'
        }}
      >
        前のページ
      </button>

      <span style={{ fontWeight: 'bold' }}>
        Page {currentPage} / {totalPages === 0 ? 1 : totalPages}
        {" "}(全 {totalCount} 件)
      </span>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={!hasNext}
        aria-label="次のページへ移動"
        style={{
          padding: '8px 16px',
          cursor: hasNext ? 'pointer' : 'not-allowed',
          opacity: hasNext ? 1 : 0.5,
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px'
        }}
      >
        次のページ
      </button>
    </div>
  );
};
