import { render, screen } from '@testing-library/react';
import App from '@/App';

describe('App', () => {
  it('renders the application header', () => {
    render(<App />);
    const headerElement = screen.getByRole('heading', {
      name: /🛒 OrderHub/i,
      level: 6,
    });
    expect(headerElement).toBeInTheDocument();
  });
});
