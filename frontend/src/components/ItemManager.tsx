import { useState } from 'react'
import { useGetItems, useCreateItem, useDeleteItem } from '../api/hooks'
import { ItemList } from './ItemList'

function ItemManager() {
  // フォーム状態
  const [newName, setNewName] = useState('')
  const [newPrice, setNewPrice] = useState('')

  // ページネーション状態
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10

  // offset計算
  const offset = (currentPage - 1) * itemsPerPage

  // TanStack Query フック（ページネーション対応）
  const { data, isLoading, error } = useGetItems({
    limit: itemsPerPage,
    offset
  })
  const createItem = useCreateItem()
  const deleteItem = useDeleteItem()

  // 新規作成（作成後は1ページ目にリセット）
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!newName || !newPrice) return

    createItem.mutate(
      { name: newName, price: Number(newPrice) },
      {
        onSuccess: () => {
          setNewName('')
          setNewPrice('')
          setCurrentPage(1)  // 1ページ目にリセット（新商品は先頭に表示されるため）
        }
      }
    )
  }

  // 削除（最後の1件を削除した場合は前ページへ）
  const handleDelete = (id: number) => {
    deleteItem.mutate(id, {
      onSuccess: () => {
        const itemsOnCurrentPage = data?.items?.length ?? 0
        // 現在ページの最後の1件を削除 & 1ページ目でない場合
        if (itemsOnCurrentPage === 1 && currentPage > 1) {
          setCurrentPage(prev => prev - 1)
        }
        // それ以外は現在ページ維持（TanStack Queryが自動再フェッチ）
      }
    })
  }

  return (
    <div className="App">
      <h1>Items管理アプリ</h1>

      {/* 新規作成フォーム */}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="名前"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <input
          type="number"
          placeholder="価格"
          value={newPrice}
          onChange={(e) => setNewPrice(e.target.value)}
        />
        <button type="submit" disabled={createItem.isPending}>
          {createItem.isPending ? '追加中...' : '追加'}
        </button>
      </form>

      {/* 一覧表示（ItemListコンポーネント使用） */}
      <ItemList
        items={data?.items ?? []}
        totalCount={data?.count ?? 0}
        currentPage={currentPage}
        itemsPerPage={itemsPerPage}
        isLoading={isLoading}
        error={error}
        onDelete={handleDelete}
        onPageChange={setCurrentPage}
      />
    </div>
  )
}

export default ItemManager
