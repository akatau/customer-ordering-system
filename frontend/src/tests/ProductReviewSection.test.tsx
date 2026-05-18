import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { Mock, vi } from 'vitest';
import ProductReviewSection from '@/components/ProductReviewSection';
import { useAuthStore } from '@stores/authStore';
import { productApi } from '@api/products';

type MockedProductApi = typeof productApi & {
  getProductReviews: Mock;
  submitReview: Mock;
};

vi.mock('@api/products', () => ({
  productApi: {
    getProductReviews: vi.fn(),
    submitReview: vi.fn(),
  },
}));

describe('ProductReviewSection', () => {
  const mockReviews = [
    {
      id: 'review-1',
      product_id: 'prod-1',
      user_id: 'user-1',
      rating: 5,
      comment: 'Excellent product! Highly recommended.',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
  ];

  beforeEach(() => {
    vi.resetAllMocks();
    useAuthStore.setState({
      user: {
        id: 'user-1',
        email: 'test@example.com',
        username: 'tester',
        full_name: 'Test User',
        role: 'customer',
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      token: 'fake-token',
    });

    (productApi as unknown as MockedProductApi).getProductReviews.mockResolvedValue({
      data: mockReviews,
      status: 200,
    });

    (productApi as unknown as MockedProductApi).submitReview.mockResolvedValue({
      data: {
        id: 'review-2',
        product_id: 'prod-1',
        user_id: 'user-1',
        rating: 4,
        comment: 'Great value for the price.',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      status: 201,
    });
  });

  afterEach(() => {
    useAuthStore.setState({ user: null, token: null });
  });

  it('loads and displays existing reviews', async () => {
    render(<ProductReviewSection productId="prod-1" />);

    expect(screen.getByText(/Customer Reviews/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/Excellent product! Highly recommended./i)).toBeInTheDocument();
    });
  });

  it('submits a new review and shows success message', async () => {
    render(<ProductReviewSection productId="prod-1" />);

    await waitFor(() => {
      expect(screen.getByText(/Excellent product! Highly recommended./i)).toBeInTheDocument();
    });

    const commentField = screen.getByLabelText(/Comment/i);
    fireEvent.change(commentField, { target: { value: 'Great value for the price.' } });

    const ratingInputs = screen.getAllByRole('radio');
    fireEvent.click(ratingInputs[3]);

    const submitButton = screen.getByRole('button', { name: /Submit Review/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Review submitted successfully/i)).toBeInTheDocument();
    });

    expect((productApi as unknown as MockedProductApi).submitReview).toHaveBeenCalledWith('prod-1', {
      rating: 4,
      comment: 'Great value for the price.',
    });
  });
});
