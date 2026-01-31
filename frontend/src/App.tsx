import { useState } from 'react'
import './App.css'
import { useGetItems, useCreateItem, useDeleteItem } from './api/hooks'

function App() {
  const [newName, setNewName] = useState('')
  const [newPrice, setNewPrice] = useState('')

  // TanStack Query フック
  const { data: items, isLoading, error } = useGetItems()
  const createItem = useCreateItem()
  const deleteItem = useDeleteItem()

  // 新規作成
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!newName || !newPrice) return

    createItem.mutate(
      { name: newName, price: Number(newPrice) },
      {
        onSuccess: () => {
          setNewName('')
          setNewPrice('')
        }
      }
    )
  }

  // 削除
  const handleDelete = (id: number) => {
    deleteItem.mutate(id)
  }

  if (isLoading) return <p>読み込み中...</p>
  if (error) return <p>エラーが発生しました</p>

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

      {/* 一覧表示 */}
      <ul>
        {items?.map((item) => (
          <li key={item.id}>
            {item.name} - ¥{item.price}
            <button onClick={() => handleDelete(item.id)}>削除</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App
