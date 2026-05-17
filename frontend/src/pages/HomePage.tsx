import { useEffect, useState } from 'react'
import Grid from '@mui/material/Grid'
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'
import FormControl from '@mui/material/FormControl'
import InputLabel from '@mui/material/InputLabel'
import Select from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import Box from '@mui/material/Box'
import { ProductCard } from '@components/ProductCard'
import { LoadingIndicator } from '@components/LoadingIndicator'
import { PageContainer } from '@components/PageContainer'
import { useProductsStore } from '@store/products'
import { useDebouncedValue } from '@hooks/useDebouncedValue'

export function HomePage() {
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [sort, setSort] = useState('')
  const debouncedSearch = useDebouncedValue(search, 400)
  const { products, categories, isLoading, error, fetchProducts, fetchCategories, searchProducts } = useProductsStore()

  useEffect(() => {
    fetchCategories()
    fetchProducts()
  }, [])

  useEffect(() => {
    if (debouncedSearch && debouncedSearch.length > 2) {
      searchProducts(debouncedSearch, sort)
    } else {
      fetchProducts(1, category, undefined, sort)
    }
  }, [debouncedSearch, category, sort])

  return (
    <PageContainer>
      <Typography variant="h4" gutterBottom>
        Browse products
      </Typography>

      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 3 }}>
        <TextField
          label="Search products"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          sx={{ minWidth: 240, flex: 1 }}
        />
        <FormControl sx={{ minWidth: 220 }}>
          <InputLabel id="category-label">Category</InputLabel>
          <Select
            labelId="category-label"
            value={category}
            label="Category"
            onChange={(event) => setCategory(event.target.value)}
          >
            <MenuItem value="">All</MenuItem>
            {categories.map((option) => (
              <MenuItem key={option} value={option}>
                {option}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ minWidth: 220 }}>
          <InputLabel id="sort-label">Sort</InputLabel>
          <Select
            labelId="sort-label"
            value={sort}
            label="Sort"
            onChange={(event) => setSort(event.target.value)}
          >
            <MenuItem value="">Featured</MenuItem>
            <MenuItem value="price_asc">Price: Low to High</MenuItem>
            <MenuItem value="price_desc">Price: High to Low</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {isLoading && <LoadingIndicator />}
      {error && <Typography color="error">{error}</Typography>}

      {!isLoading && !error && (
        <Grid container spacing={3}>
          {products.length === 0 ? (
            <Grid item xs={12}>
              <Typography>No products found.</Typography>
            </Grid>
          ) : (
            products.map((product) => (
              <Grid item key={product.id} xs={12} sm={6} md={4}>
                <ProductCard product={product} />
              </Grid>
            ))
          )}
        </Grid>
      )}
    </PageContainer>
  )
}
