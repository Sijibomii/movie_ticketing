import React,{ useState } from 'react';
import './sass/main.scss'
import axios from 'axios'
import HomeScreen from './screens/HomeScreen'
import MovieScreen from './screens/MovieScreen'
import ScreeningScreen from './screens/ScreeningScreen'
import Header from './components/Header'
import Footer from './components/Footer'
import LoginScreen from './screens/LoginScreen'
import SignupScreen from './screens/SignupScreen'
import DashboardScreen from './screens/DashboardScreen'
import CartScreen from './screens/CartScreen'
import AllScreenings from './screens/AllScreenings'
import { BrowserRouter as Router, Route, Switch,Redirect} from 'react-router-dom'

function App() {
  
  const [isLoggedIn, setLoggedIn] = useState(() => {
    return window.localStorage.getItem('taxi.auth') !== null;
  });
  const logOut = () => {
    window.localStorage.removeItem('taxi.auth');
    setLoggedIn(false);
   
  };
  
  const logIn = async (username, password) => {
    const url = `http://localhost:8000/api/log_in/`;
    try {
      const response = await axios.post(url, { username, password });
      window.localStorage.setItem(
        'taxi.auth', JSON.stringify(response.data)
      );
      setLoggedIn(true);
      return { response, isError: false };
    }
    catch (error) {
      console.error(error);
      return { response: error, isError: true };
    }
  };
  return (
    <>
     <Router>
        <Header logout={logOut} isLoggedIn={isLoggedIn} />
          <Switch>
            <Route path='/allscreenings' component={AllScreenings} exact/>
            <Route path='/dashboard' render={()=>(
              isLoggedIn ?(
                <DashboardScreen isLoggedIn={isLoggedIn}/>
              ):(
                <Redirect to='/sign-in' />
              )
            )}exact/>
            <Route path='/cart' render={()=>(
              isLoggedIn ?(
                <CartScreen isLoggedIn={isLoggedIn}/>
              ):(
                <Redirect to='/sign-in' />
              )
            )}exact/>
            <Route path='/screening/:id' render={props=>(
              <ScreeningScreen isLoggedIn={isLoggedIn}/>
            )} exact/>
            <Route path='/sign-up' render={() => (
            isLoggedIn ? (
              <Redirect to='/' />
            ) : (
              <SignupScreen />
            )
          )} />
          <Route path='/sign-in' render={() => (
            isLoggedIn ? (
              <Redirect to='/' />
            ) : (
              <LoginScreen logIn={logIn} exact/>
            )
          )} />
            
            <Route  path='/movie/:id' component={MovieScreen} exact/>
            <Route  path='/' component={HomeScreen} exact/>
          </Switch>
        <Footer />
      </Router>
    </>
  );
}

export default App;
