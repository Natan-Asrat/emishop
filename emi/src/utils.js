export const getPostData = (post) => ({
  id: post.id,
  name: post.title,
  price: parseFloat(post.price),
  image: post.images[0],
  images: post.images,
  stockLeft: post.quantity,
  totalStock: post.initial_quantity,
  liked: post.liked,
  quantity: 1,
  isActive: post.is_active,
  description: post.title,
  sellerName: post.created_by.username,
  sellerAvatar: "https://placehold.co/40",
  postedDate: new Date(post.created_at).toLocaleDateString(),
  embedding: post.embedding
})