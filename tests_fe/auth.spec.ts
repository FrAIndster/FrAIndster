const request = require('supertest');
const app = require('./app');  // Import the app

describe('POST /login', () => {
  it('should return 200 if credentials are correct', async () => {
    const response = await request(app)
      .post('/login')
      .send({ username: 'testuser', password: 'password123' });

    expect(response.status).toBe(200);
    expect(response.body.message).toBe('Login successful');
  });

  it('should return 401 if credentials are incorrect', async () => {
    const response = await request(app)
      .post('/login')
      .send({ username: 'testuser', password: 'wrongpassword' });

    expect(response.status).toBe(401);
    expect(response.body.message).toBe('Invalid credentials');
  });

  it('should return 401 if no credentials are provided', async () => {
    const response = await request(app)
      .post('/login')
      .send({});

    expect(response.status).toBe(401);
    expect(response.body.message).toBe('Invalid credentials');
  });
});