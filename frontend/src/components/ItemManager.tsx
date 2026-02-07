import { useState } from 'react'
import { useGetItems, useCreateItem, useUpdateItem, useDeleteItem, useLogout } from '../api/hooks'
import { ItemList } from './ItemList'
import type { components } from '../api/schema'

type ItemSchema = components["schemas"]["ItemSchema"]

function ItemManager() {
  // フォーム状態
  const [newName, setNewName] = useState('')
  const [newPrice, setNewPrice] = useState('')

  // ページネーション状態
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10

  // offset計算
  const offset = (currentPage - 1) * itemsPerPage

  // 編集状態
  const [editingItem, setEditingItem] = useState<ItemSchema | null>(null)

  // TanStack Query フック（ページネーション対応）
  const { data, isLoading, error } = useGetItems({
    limit: itemsPerPage,
    offset
  })
  const createItem = useCreateItem()
  const updateItem = useUpdateItem()
  const deleteItem = useDeleteItem()
  const logout = useLogout()

  // 編集開始
  const handleEdit = (item: ItemSchema) => {
    setEditingItem(item)
    setNewName(item.name)
    setNewPrice(String(item.price))
  }

  // 編集キャンセル
  const handleCancelEdit = () => {
    setEditingItem(null)
    setNewName('')
    setNewPrice('')
  }

  // 新規作成 or 更新
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!newName || !newPrice) return

    if (editingItem) {
      updateItem.mutate(
        { itemId: editingItem.id, data: { name: newName, price: Number(newPrice) } },
        {
          onSuccess: () => {
            setEditingItem(null)
            setNewName('')
            setNewPrice('')
          }
        }
      )
    } else {
      createItem.mutate(
        { name: newName, price: Number(newPrice) },
        {
          onSuccess: () => {
            setNewName('')
            setNewPrice('')
            setCurrentPage(1)
          }
        }
      )
    }
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
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Items管理アプリ</h1>
        <button
          type="button"
          onClick={() => logout.mutate()}
          disabled={logout.isPending}
          style={{
            backgroundColor: '#6c757d',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            padding: '8px 16px',
            cursor: logout.isPending ? 'not-allowed' : 'pointer',
          }}
        >
          {logout.isPending ? 'ログアウト中...' : 'ログアウト'}
        </button>
      </div>

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
        <button type="submit" disabled={editingItem ? updateItem.isPending : createItem.isPending}>
          {editingItem
            ? (updateItem.isPending ? '更新中...' : '更新')
            : (createItem.isPending ? '追加中...' : '追加')
          }
        </button>
        {editingItem && (
          <button type="button" onClick={handleCancelEdit}>
            キャンセル
          </button>
        )}
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
        onEdit={handleEdit}
        onPageChange={setCurrentPage}
      />
    </div>
  )
}

export default ItemManager
