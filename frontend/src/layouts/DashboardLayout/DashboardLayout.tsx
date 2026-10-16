import { Outlet } from 'react-router-dom'

import Header from '../../components/common/Header/Header'
import Sidebar from '../../components/common/Sidebar/Sidebar'
import Footer from '../../components/common/Footer/Footer'

import './DashboardLayout.css'

function DashboardLayout() {
  return (
    <div className="dashboard-layout">

      <Header />

      <div className="dashboard-layout__body">

        <Sidebar />

        <main className="dashboard-layout__content">
          <Outlet />
        </main>

      </div>

      <Footer />

    </div>
  )
}

export default DashboardLayout