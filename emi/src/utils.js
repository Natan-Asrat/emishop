export const getPostData = (post) => {
    return {
        id: post.id,
        name: post.title,
        price: parseFloat(post.price),
        image: post.images[0],
        images: post.images, // Assuming single image for now
        stockLeft: post.quantity,
        totalStock: post.initial_quantity,
        liked: post.liked,
        quantity: 1,
        isActive: post.is_active,
        description: post.title, // You might want to add description field in your model
        sellerName: post.created_by.username,
        sellerAvatar: "https://placehold.co/40", // You might want to add avatar in your UserProfile
        postedDate: new Date(post.created_at).toLocaleDateString(),
        embedding: post.embedding
      }
}