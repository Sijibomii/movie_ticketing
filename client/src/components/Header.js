import React,{ useState, useEffect }  from 'react'
import { Link } from 'react-router-dom'
import { getUser } from '../services/AuthService'
const Header = ({ logout, isLoggedIn}) => {
  const [user,setUser]=useState('')
  useEffect(() => {
   setUser(getUser())
   console.log(user)
  }, [])
  return (
    <header className="header" id="header">
      <div className="header__container">
        <div className="header__logo">
          <h1><Link to='/'>CINEMA</Link></h1>
        </div>
        <div className="header__links">
          <ul>
            { isLoggedIn && user ? (
              <>
              <Link to='/dashboard'><li>{user.username}</li></Link>
              <Link to='/cart'><h2>Cart</h2><i class="fas fa-shopping-cart fa-2x"></i></Link>
              <li className='logout' onClick={()=>{
                return logout()
              }}>Logout</li>
              </>
            ):<Link to='/sign-in'><li>Sign in</li></Link>
            }
           
          </ul>
        </div>
      </div>
    </header> 
  )
}

export default Header
