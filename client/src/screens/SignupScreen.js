import React, { useState } from 'react'
import { Formik } from 'formik';
import { ToastContainer, toast } from 'react-toastify';
import { Link, Redirect } from 'react-router-dom'
// import 'react-toastify/dist/ReactToastify.css';
import axios from 'axios';
const SignupScreen = () => {
  const [error, setError]= useState('')
  const [isSubmitted, setSubmitted] = useState(false);
   const onSubmit = async (values) => {
    const url = `http://localhost:8000/api/sign_up/`;
    const formData = new FormData();
    formData.append('username', values.username);
    formData.append('first_name', values.firstName);
    formData.append('last_name', values.lastName);
    formData.append('password1', values.password);
    formData.append('password2', values.password);
    try {
      await axios.post(url, formData);
      setSubmitted(true);
    }
    catch (response) {
      console.log(response)
      setError('Invalid entries')
      // const data = response.response.data;
      // console.log(data)
      // for (const value in data) {
      //   actions.setFieldError(value, data[value].join(' '));
      // }
    }
  };
   if (isSubmitted) {
     return <Redirect to='/sign-in' />
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
              firstName: '',
              lastName: '',
              password: '',
            }}
            onSubmit={onSubmit}
          >
            {({
              errors,
              handleChange,
              handleSubmit,
              isSubmitting,
              setFieldValue,
              values
            }) => (
            <form noValidate onSubmit={handleSubmit}>
              <input 
              placeholder="username" 
              name='username'
              onChange={handleChange}
              values={values.username}
              required
              />
              <input 
              placeholder="Enter first name"
              name='firstName'
              onChange={handleChange}
              values={values.firstName}
              />
              <input 
              placeholder="Enter last name name"
              name='lastName'
              onChange={handleChange}
              values={values.lastName}
              />
              <input
                  type="password"
                  autoComplete="off"
                  placeholder="Password"
                  name='password'
                  onChange={handleChange}
                  type='password'
                  value={values.password}
                />
              
          
              <Link className="submit" type="submit" onClick={()=>{
              return onSubmit(values)
            }}>Submit</Link>
            </form>
            )}
          </Formik>
        
        <h3 className="text">An existing customer? <Link to="/sign-in" className='red'>Sign in now.</Link></h3>
    </div>
    </div>
  )
}

export default SignupScreen
