import React,{ useState,useEffect} from 'react'
import { ToastContainer, toast } from 'react-toastify';
import { Link } from "react-router-dom";
import { getMovie } from '../services/MovieService';
import { getScreeningByMovie} from '../services/ScreeningService'
const MovieScreen = ({ match }) => {
  const[screening, setScreening] =useState([])
  const [movie, setMovie]=useState({})
  useEffect(()  => {
    const loadMovie = async () => {
      const { response, isError } = await getMovie(match.params.id);
      if (isError) {
        setMovie([]);
      } else {
        // console.log(response.data)
        setMovie(response.data);
      }
    }
    loadMovie();
  }, [])
  useEffect(()  => {
    const loadScreening = async () => {
      const { response, isError } = await getScreeningByMovie(match.params.id);
      if (isError) {
        setScreening([]);
      } else {
        // console.log(response.data)
        setScreening(response.data);
      }
    }
    loadScreening();
  }, [])
  const style={
    background: `linear-gradient(to bottom, rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.35)),url(${movie.image}) top left / cover no-repeat`
  }
  return (
    <>
     <ToastContainer />
      <div id="myModal" class="modal">
        <div class="modal-content">
          <span class="close">&times;</span>
          
        </div>
      </div>
      <div className="movie" style={style}>
          <div className="movie__stats">
            <h1>{movie.title}</h1>
            <div className="movie__stats__rating">
              <i class="fas fa-star fa-5x"></i>
              <i class="fas fa-star fa-5x"></i>
              <i class="fas fa-star fa-5x"></i>
              <i class="fas fa-star fa-5x"></i>
              <i class="far fa-star fa-5x"></i>
            </div>
            <h3>{movie.genre}| Drama</h3>
            <h4>{movie.duration}</h4>
            <h4 className="direct">Directed by: {movie.director}</h4>
            <div className="movie__stats__buttons">
              {/* <a className="d-sm-none" id="mybtn" onClick={openModal}><i class="fas fa-play "></i></a> */}
              <Link>BOOK A TICKET</Link>
            </div>
          </div>
      </div>
      <div className="showing__times">
        <h1>Showing Times</h1>
        
          {screening.length==0 ?(
            <h2>No Screenings available</h2>
          ):<>
          {screening.map((screen)=>(
          <div className="showing__times__time" key={screen.id}>
            <div className="showing__times__time__datetime">
              <h4>{screen.date}</h4>
              <h4>{screen.time}</h4>
            </div>
            <div className="showing__times__time__button">
              <a href={`/screening/${screen.id}`}>BOOK A SEAT</a>
            </div>
          </div>
          ))}
          </>}
      </div>
    </>
  )
}

export default MovieScreen
