import axios from 'axios';
import { share } from 'rxjs/operators'; 
import { webSocket } from 'rxjs/webSocket'; 
import { getAccessToken,getUser } from './AuthService';
import FileDownload from 'js-file-download';
let _socket;
export let messages;

export const connect = () => {
  if (!_socket || _socket.closed) {
    const token = getAccessToken();
    _socket = webSocket(`ws://localhost:8000/movie/?token=${token}`);
    messages = _socket.pipe(share());
    messages.subscribe(message => console.log(message));
  }
};

export const connectToScreening = (id) => {
  connect();
  let data={
    group: id
  }
  const message = {
    type: 'add.group',
    data: data
  };
  _socket.next(message);
};

export const assignSeat = (id, data) => {
  connectToScreening(id);
  const message = {
    type: 'assign.seat',
    data: data
  };
  _socket.next(message);
};

export const removeSeat = (id, data) => {
  connectToScreening(id);
  console.log('yes')
  console.log(data)
  const message = {
    type: 'remove.seat',
    data: data
  };
  _socket.next(message);
};
export const getScreenings = async () => {
  const url = `http://localhost:8000/api/movie/screenings/all/`;
  try {
    const response = await axios.get(url);
    return { response, isError: false };
  } catch (response) {
    return { response, isError: true };
  }
};

export const getScreeningByMovie = async (id) => {
  const url = `http://localhost:8000/api/movie/screening/movie/${id}/`;
  try {
    const response = await axios.get(url);
    return { response, isError: false };
  } catch (response) {
    return { response, isError: true };
  }
};

export const getSeatsByScreening = async (id) => {
  const url = `http://localhost:8000/api/seats/screening/${id}/`;
  try {
    const response = await axios.get(url);
    return { response, isError: false };
  } catch (response) {
    return { response, isError: true };
  }
};

export const getSeatsAssigned = async () => {
  const url = `http://localhost:8000/api/seats/`;
  const token = getAccessToken();
  const headers = { Authorization: `Bearer ${token}` };
  try {
    const response = await axios.get(url, { headers });
    return { response, isError: false };
  } catch (response) {
    return { response, isError: true };
  }
};
export const getSeatsPay = async () => {
  const user=getUser()
  const url = `http://localhost:8000/api/seats/screening/pay/${user.id}/`;
  const token = getAccessToken();
  const headers = { Authorization: `Bearer ${token}` };
  try {
    const response = await axios.post(url, { headers });
    return { response, isError: false };
  } catch (response) {
    return { response, isError: true };
  }
};

export const getDownloadTicket = async (id) => {
  
  const url = `http://localhost:8000/api/tickets/${id}/`;
  const token = getAccessToken();
  const headers = { Authorization: `Bearer ${token}` };

  try {
    const response = await axios.post(url,{ headers });
    const blob = new Blob([response.data]);
    FileDownload(blob, `ticket${id}.png`);
    return { response, isError: false };
  } catch (response) {
    return { response, isError: true };
  }
};

export const getSeatsBooked = async () => {
  const url = `http://localhost:8000/api/seats/booked/`;
  const token = getAccessToken();
  const headers = { Authorization: `Bearer ${token}` };
  try {
    const response = await axios.get(url, { headers });
    
    return { response, isError: false };
  } catch (response) {
    return { response, isError: true };
  }
};