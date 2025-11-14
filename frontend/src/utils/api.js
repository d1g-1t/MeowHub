import { API_BASE_URL } from "./constants";

const getToken = () => localStorage.getItem("auth_token");

const buildHeaders = (withAuth = false, extra = {}) => {
  const headers = {
    "Content-Type": "application/json",
    ...extra,
  };
  if (withAuth) {
    const token = getToken();
    if (token) {
      headers.authorization = `Token ${token}`;
    }
  }
  return headers;
};

const handleResponse = async (response) => {
  if (response.status === 204) {
    return null;
  }
  const payload = await response.json();
  if (!response.ok) {
    throw payload;
  }
  return payload;
};

const request = (endpoint, options = {}) =>
  fetch(`${API_BASE_URL}${endpoint}`, options).then(handleResponse);

export const registerUser = (username, password) =>
  request("/api/users/", {
    method: "POST",
    headers: buildHeaders(),
    body: JSON.stringify({ username, password }),
  });

export const loginUser = (username, password) =>
  request("/api/token/login/", {
    method: "POST",
    headers: buildHeaders(),
    body: JSON.stringify({ username, password }),
  }).then((data) => {
    if (data?.auth_token) {
      localStorage.setItem("auth_token", data.auth_token);
      return data;
    }
    return null;
  });

export const logoutUser = () =>
  request("/api/token/logout/", {
    method: "POST",
    headers: buildHeaders(true),
  }).then(() => {
    localStorage.removeItem("auth_token");
    return null;
  });

export const getUser = () =>
  request("/api/users/me/", {
    headers: buildHeaders(true),
  });

export const getCards = (page = 1) =>
  request(`/api/cats/?page=${page}`, {
    headers: buildHeaders(true),
  });

export const getCard = (id) =>
  request(`/api/cats/${id}/`, {
    headers: buildHeaders(true),
  });

export const getAchievements = () =>
  request(`/api/achievements/`, {
    headers: buildHeaders(true),
  });

export const sendCard = (card) =>
  request(`/api/cats/`, {
    method: "POST",
    headers: buildHeaders(true),
    body: JSON.stringify(card),
  });

export const updateCard = (card, id) =>
  request(`/api/cats/${id}/`, {
    method: "PATCH",
    headers: buildHeaders(true),
    body: JSON.stringify(card),
  });

export const deleteCard = (id) =>
  request(`/api/cats/${id}/`, {
    method: "DELETE",
    headers: buildHeaders(true),
  });
