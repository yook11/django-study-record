import { Routes, Route, Navigate } from 'react-router-dom';
import ItemManager from './components/ItemManager';
import Login from './components/Login';
import './App.css'

function App() {
  return (
    <>
      <Routes>
        {/* 1. ログイン画面 */}
        <Route path="/login" element={<Login />} />

        {/* 2. 商品管理画面 */}
        <Route path="/items" element={<ItemManager />} />

        {/* 3. トップページに来たら /items に飛ばす */}
        <Route path="/" element={<Navigate to="/items" replace />} />
      </Routes>
    </>
  )
}

export default App
