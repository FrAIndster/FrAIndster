import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { api } from '../../services/api';

export const generateProfile = createAsyncThunk(
  'profile/generate',
  async () => {
    const response = await api.post('/profiles/generate_profile/');
    return response.data;
  }
);

const profileSlice = createSlice({
  name: 'profile',
  initialState: {
    profiles: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(generateProfile.pending, (state) => {
        state.loading = true;
      })
      .addCase(generateProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.profiles.push(action.payload);
      })
      .addCase(generateProfile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default profileSlice.reducer; 