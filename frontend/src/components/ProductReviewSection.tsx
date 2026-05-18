import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Rating,
  TextField,
  Button,
  Alert,
  Paper,
  Stack,
  Divider,
  CircularProgress,
} from '@mui/material';
import { useAuthStore } from '@stores/authStore';
import { productApi } from '@api/products';
import { Review, ReviewRequest } from '@/types';

interface ProductReviewSectionProps {
  productId: string;
}

const ProductReviewSection: React.FC<ProductReviewSectionProps> = ({ productId }) => {
  const { user } = useAuthStore();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [rating, setRating] = useState<number | null>(0);
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);
  const [submitLoading, setSubmitLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const loadReviews = async () => {
    setLoading(true);
    setError('');
    const response = await productApi.getProductReviews(productId, 1);
    setLoading(false);

    if (response.error) {
      setError(response.error.detail);
      return;
    }

    setReviews(response.data || []);
  };

  useEffect(() => {
    if (!productId) {
      return;
    }

    loadReviews();
  }, [productId]);

  const handleSubmitReview = async () => {
    setError('');
    setSuccess('');

    if (!user) {
      setError('Please log in to submit a review.');
      return;
    }

    if (!rating || rating < 1) {
      setError('Please select a star rating.');
      return;
    }

    if (!comment.trim()) {
      setError('Please enter a review comment.');
      return;
    }

    setSubmitLoading(true);
    const payload: ReviewRequest = { rating, comment: comment.trim() };
    const response = await productApi.submitReview(productId, payload);
    setSubmitLoading(false);

    if (response.error) {
      setError(response.error.detail);
      return;
    }

    setSuccess('Review submitted successfully. Thank you!');
    setRating(0);
    setComment('');
    loadReviews();
  };

  const averageRating =
    reviews.length > 0
      ? reviews.reduce((sum, review) => sum + review.rating, 0) / reviews.length
      : 0;

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Customer Reviews
      </Typography>

      <Typography variant="body2" color="textSecondary" sx={{ mb: 3 }}>
        Share your buying experience, read other customers' feedback, and help shoppers decide.
      </Typography>

      <Paper sx={{ p: 3, mb: 3, bgcolor: '#fafafa' }}>
        <Stack spacing={1}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Rating value={averageRating} precision={0.5} readOnly />
            <Typography variant="body2" color="textSecondary">
              {reviews.length > 0 ? `${averageRating.toFixed(1)} average rating` : 'No reviews yet'}
            </Typography>
          </Box>
          <Typography variant="body2" color="textSecondary">
            {reviews.length} review{reviews.length === 1 ? '' : 's'}
          </Typography>
        </Stack>
      </Paper>

      {loading ? (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Stack spacing={2} sx={{ mb: 3 }}>
          {reviews.length === 0 ? (
            <Alert severity="info">No reviews have been posted for this product yet.</Alert>
          ) : (
            reviews.map((review) => (
              <Paper key={review.id} sx={{ p: 3 }}>
                <Stack spacing={1}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Rating value={review.rating} readOnly size="small" />
                    <Typography variant="body2" color="textSecondary">
                      {new Date(review.created_at).toLocaleDateString()}
                    </Typography>
                  </Box>
                  <Typography variant="body1">{review.comment}</Typography>
                </Stack>
              </Paper>
            ))
          )}
        </Stack>
      )}

      <Divider sx={{ mb: 3 }} />

      <Box component={Paper} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Write a Review
        </Typography>
        <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
          Reviews are verified against purchase history. If you have ordered this product, submit your rating and comment below.
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

        <Stack spacing={2}>
          <Box>
            <Typography component="label" variant="subtitle2" htmlFor="review-rating" sx={{ mb: 1, display: 'block' }}>
              Rating
            </Typography>
            <Rating
              id="review-rating"
              name="review-rating"
              value={rating}
              onChange={(_, value) => setRating(value)}
              precision={1}
            />
          </Box>

          <TextField
            label="Comment"
            multiline
            minRows={4}
            value={comment}
            onChange={(event) => setComment(event.target.value)}
            placeholder="Tell us what you liked and what can improve."
            fullWidth
          />

          <Button
            variant="contained"
            color="primary"
            onClick={handleSubmitReview}
            disabled={submitLoading}
          >
            {submitLoading ? 'Submitting...' : 'Submit Review'}
          </Button>
        </Stack>
      </Box>
    </Box>
  );
};

export default ProductReviewSection;
