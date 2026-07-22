import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getSystemHealth = async () => {
  const res = await api.get('/');
  return res.data;
};

export const getRecipes = async (params = {}) => {
  const res = await api.get('/recipes', { params });
  return res.data;
};

export const getRecipeById = async (id) => {
  const res = await api.get(`/recipe/${id}`);
  return res.data;
};

export const searchRecipes = async (searchPayload) => {
  const res = await api.post('/search', searchPayload);
  return res.data;
};

export const recommendRecipes = async (recommendPayload) => {
  const res = await api.post('/recommend', recommendPayload);
  return res.data;
};

export const getCuisines = async () => {
  const res = await api.get('/cuisines');
  return res.data;
};

export const getMealTypes = async () => {
  const res = await api.get('/meal-types');
  return res.data;
};

export const autocompleteIngredients = async (query) => {
  const res = await api.get('/ingredients/autocomplete', { params: { q: query } });
  return res.data;
};

export default api;
