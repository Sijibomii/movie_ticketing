import React from 'react'
import Slider from 'react-slick'
const Sliderr = ({movies}) => {
  //console.log(movies)
  const width=window.screen.width
  let show=3
  if(width< 600){
    show=1
  }
  else if(width< 900){
    show=2
  }
  else{
    show=3
  }
  let settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: show,
    slidesToScroll: 1
  };
 
  return (
    <>
    <div className="slider__section">
      <h2 id="featured">ALL FEATURED MOVIES</h2>
      <h3 id="showing-now">Now Showing</h3>
      <Slider {...settings}>
        {movies.map((movie)=>(
          <div className="card" key={movie.id}>
            <div className="card__top">
              <img src={movie.image} className="cardd-img"/>
            </div>
            <div className="card__below">
              <h3>{movie.title}</h3>
              <h4>{movie.duration} | {movie.rated}</h4>
              <h4>Released Aug 20</h4>
              <a>BOOK TICKET</a>
            </div>
          </div>
        ))}
        
        {/* <div className="card">
          <div className="card__top">
            <img src='http://localhost:8000/media/photos/2021/01/23/small.jpg' className="cardd-img"/>
          </div>
          <div className="card__below">
            <h3>King Of Boys</h3>
            <h4>1hr 30min | 18+</h4>
            <h4>Released Aug 20</h4>
            <a>BOOK TICKET</a>
          </div>
        </div>
        <div className="card">
          <div className="card__top">
            <img src='./images/series/children/arthur/small.jpg' className="cardd-img"/>
          </div>
          <div className="card__below">
            <h3>King Of Boys</h3>
            <h4>1hr 30min | 18+</h4>
            <h4>Released Aug 20</h4>
            <a>BOOK TICKET</a>
          </div>
        </div>
        <div className="card">
          <div className="card__top">
            <img src='./images/series/children/arthur/small.jpg' className="cardd-img"/>
          </div>
          <div className="card__below">
            <h3>King Of Boys</h3>
            <h4>1hr 30min | 18+</h4>
            <h4>Released Aug 20</h4>
            <a>BOOK TICKET</a>
          </div>
        </div> */}
        {/* <div className="card">
          <div className="card__top">
            <img src='./images/series/children/arthur/small.jpg' className="cardd-img"/>
          </div>
          <div className="card__below">
            <h3>King Of Boys</h3>
            <h4>1hr 30min | 18+</h4>
            <h4>Released Aug 20</h4>
            <a>BOOK TICKET</a>
          </div>
        </div> */}
      </Slider>
    </div>
    </>
  )
}

export default Sliderr
