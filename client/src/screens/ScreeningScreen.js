import React,{ useEffect,useState } from 'react'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { getSeatsByScreening, messages,connectToScreening , assignSeat} from '../services/ScreeningService'
import { Link } from 'react-router-dom'
import { getUser } from '../services/AuthService'
import { withRouter }from 'react-router-dom'
const ScreeningScreen = ({ match,history,isLoggedIn }) => {
  const[seats, setSeats]=useState([])
  const[rawSeats,setRawSeats]= useState([])
  useEffect(()  => {
     
    const loadSeats = async () => {
      if(!isLoggedIn){
        console.log('dfghjk');
        history.push('/sign-in')
        // <Redirect to='/sign-in' />
      }
      console.log(isLoggedIn)
      const { response, isError } = await getSeatsByScreening(match.params.id);
      if (isError) {
        setSeats([]);
      } else {
        setRawSeats(response.data)
        submitHandler(response.data);
      }
    }
    loadSeats();
  }, [isLoggedIn])
  useEffect(() => {
    connectToScreening(match.params.id);
    const subscription = messages.subscribe((message) => {
      console.log('connected')
      loadSeats()
      if (rawSeats.length!=0 && message.data.id){
        console.log('change')
        console.log(message.data.id)
        changeSeat(message.data.id,message.data.status);
      }
      if (message.data.status =='EMPTY'){
        toast.info(`seat ${message.data.id} is now free!!!`)
      }
     
    });
    return () => {
      if (subscription) {
        subscription.unsubscribe();
      }
    }
  }, []);
  const loadSeats = async () => {
    const { response, isError } = await getSeatsByScreening(match.params.id);
    if (isError) {
      setSeats([]);
    } else {
      setRawSeats(response.data)
      submitHandler(response.data);
    }
  }
  const changeSeat = (id, status)=>{
    const seat=rawSeats.map((seat)=>{
      if (seat.id == id){
        seat.status=status
      }
    })
    submitHandler(rawSeats)
  }
  const submitHandler = (arr) => {
    let bigArr=[]
    let newArr=[]
    for (let i=0; i<=(arr.length/10); i++){
      let end= ((i*10)+10)
      newArr= arr.slice((i*10), end)
      bigArr.push(newArr)
      newArr=[]
    }
    setSeats(bigArr)
  }
  const asignSeatsStatus = (id) => {
    const user = getUser();
    const data={
      screening: match.params.id,
      user: user.id,
      seat: id,
      status: 'ASSIGNED'
    }
    console.log(data)
    assignSeat(match.params.id, data);
   
  };
  
  return (
    <>
    <div className="screening">
      <ToastContainer/>
      <div className="movie-container">
        <h3></h3>
      </div>
      <p>Users have 10 minutes to complete check out process else, all Temporarily assigned seats will be declared empty</p>

    <ul className="showcase">
      <li>
        <div className="seat"></div>
        <small>N/A</small>
      </li>
      <li>
        <div className="seat selected"></div>
        <small>Selected</small>
      </li>
      <li>
        <div className="seat occupied"></div>
        <small>Occupied</small>
      </li>
      <li>
        <div className="seat temporary"></div>
        <small>Temporarily assined to a user</small>
      </li>
    </ul>

    <div className="container">
      <div className="screen"></div>
        {seats.map((seat)=>(
          <>
          <div className="row">
          {seat.map((s)=>(
            <>
            
            <div className={s.status==="EMPTY"? 'seat': s.status==="ASSIGNED" ? 'seat temporary' : 'seat occupied'} key={seat.id} onClick={()=>{
              if(s.status==='EMPTY'){
                //
                asignSeatsStatus(s.id)
                toast.info('seat is has been added to your cart, please ensure you complete checkout within 10min')
              }
              else{
                if(s.status==='ASSIGNED'){
                  toast.info('seat is currently assigned to someone, please check back')
                }
                else{
                  toast.info('seat is has been booked by a user')
                }
              }
            }}></div>
            </>
          ))}
          </div>
          </>
        ))}
    </div>

    {/* <p className="text">
      You have selected <span id="count">0</span> seats
    </p> */}
      <Link className="checkout__button" to='/cart'>CHECKOUT NOW</Link>
    </div>
    
    </>
  )
}

export default withRouter(ScreeningScreen)
