import React,{ useState, useEffect } from 'react'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { removeSeat,connectToScreening,getSeatsAssigned,messages, getSeatsPay} from '../services/ScreeningService'
import { getUser } from '../services/AuthService'
import { Link } from 'react-router-dom';

const CartScreen = ({ isLoggedIn, history }) => {
  const[seats, setSeats]=useState([])
 
  useEffect(()  => {
    const loadSeats = async () => {
      if(!isLoggedIn){
        history.push('/sign-in')
        // 
      }
      const { response, isError } = await getSeatsAssigned();
      if (isError) {
        setSeats([]);
      } else {
        console.log(response.data)
        setSeats(response.data);
      }
    }
    loadSeats();
  }, [])
  const payHandler = async ()=>{
    const { response, isError } = await getSeatsPay();
    if(isError){
      toast.info('Error occured')
    }else{
      window.location.replace("/dashboard");
      
    }
  }
  const loadSeats = async () => {
    const { response, isError } = await getSeatsAssigned();
    if (isError) {
      setSeats([]);
    } else {
      setSeats(response.data)
    }
  }
  const util=(screen, seat)=>{
   
    connectToScreening(screen);
    const subscription = messages.subscribe((message) => {
      const { id }=getUser()
      let data={
          screening: screen,
          user: id,
          seat: seat,
          status: 'EMPTY'
      }
      removeSeat(screen,data)
      loadSeats()
    });
    return () => {
      if (subscription) {
        subscription.unsubscribe();
      }
    }
  }
  return (
    <>
    <div>
      </div>
      <div className="cart">
      <ToastContainer />
        <div className="cart__container">
          <h1>CART ITEMS</h1>
              {seats.length ==0 ?(
            <>
            <h3>Your Cart Is Empty</h3>
            </>
          ):
              <>
          {seats.map((seat)=>(
            <>
          <div className="cart__container__item" key={seat.id}>
            <div className="cart__container__item__top">
              <h2>Movie: {seat.screening.movie.title} </h2>
              <h3>Seat No: {seat.id}</h3>
              <h4>Venue: {seat.screening.venue.name}</h4>
              <h4>Price : $ {seat.screening.price}</h4>
            </div>
            <div className="cart__container__item__bottom">
              <i class="fas fa-trash fa-6x" onClick={()=>{
                util(seat.screening.id, seat.id)
                toast.info('Seat Removed!')
              }}></i>
            </div>
          </div>
            </>
          ))}
          </>
          }
        <Link className="checkout__button" onClick={()=>{
          return payHandler()
        }}>CHECKOUT NOW</Link>
        </div>
      </div>
    </>
  )
}

export default CartScreen
