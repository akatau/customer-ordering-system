import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { PageContainer } from '@components/PageContainer'

describe('PageContainer', () => {
  it('renders its children inside the container', () => {
    render(
      <PageContainer>
        <span>QA smoke test</span>
      </PageContainer>
    )

    expect(screen.getByText('QA smoke test')).toBeInTheDocument()
  })
})