import { render, screen } from '@testing-library/react';
import App from '@/App';

describe('App', () => {
  it('renders the application header', async () => {
    render(<App />);
    const headerElement = await screen.findByRole('heading', {
      name: /🛒 OrderHub/i,
      level: 6,
    });
    expect(headerElement).toBeInTheDocument();
  });
});
