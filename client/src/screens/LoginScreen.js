import React, { useState, useEffect } from 'react'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Formik } from 'formik'
import { Link } from 'react-router-dom';

// import { useDispatch, useSelector } from 'react-redux'
// import { login } from '../actions/userActions'
const LoginScreen = ({ logIn }) => {
  const [error, setError]= useState('')
  const onSubmit = async (values) => {
    try {
      const { response, isError } = await logIn(
        values.username,
        values.password
      );
      if (isError) {
        if (JSON.stringify(response).includes('Error')){
          setError('Invalid Login Details')
        }
        const data = response.response.data;
        if(data.username && data.password){
          let str='username and password fields are required'
          setError(str)
        }
        else if(data.username){
          let str='username:'
          setError(str.concat(data['username'][0]))
        }else if(data.password){
          let str='password:'
          setError(str.concat(data['password'][0]))
    
        }
      }
    }
    catch (error) {
      console.error(error);
    }
  } 
  return (
    <div className="login">
     
       <ToastContainer />
      <div className="login__container">
        <h1 className="form__title">Sign in</h1>
        { error && (
          <h3 className="errors">{error}</h3>
        )}
        
        <Formik
            initialValues={{
              username: '',
              password: ''
            }}
            onSubmit={onSubmit}
          >
            {({
               errors, 
               handleChange,
               handleSubmit,
               isSubmitting, 
              values
            }) => (
            <>
              {
                '__all__' in errors &&
                console.log('dkk')
                // <Alert variant='danger'>
                //   { errors['__all__'] }
                // </Alert>
              }
          <form noValidate onSubmit={handleSubmit}>
            <input 
            name='username'
            placeholder="Username"
            onChange={handleChange}
            value={values.username}
            />
            <input
                name='password'
                placeholder="password"
                type="password"
                autoComplete="off"
                onChange={handleChange}
                type='password'
                value={values.password}
              />
            <Link className="submit"type="submit" onClick={()=>{
              return onSubmit(values)
            }}>Submit</Link>
        </form>
        </>
        )} 
      </Formik>
        <h3 className="text">New to our website? <Link to="/sign-up" className='red'>Sign up now.</Link></h3>
    </div>
    </div>
  )
} 

export default LoginScreen
