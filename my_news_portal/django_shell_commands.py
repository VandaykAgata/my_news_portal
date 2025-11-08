# С. Комментарии к этой статье
print('\n--- Комментарии к лучшей статье ---')
comments = Comment.objects.filter(post=best_post).values('user__username', 'rating', 'text')
for comment in comments:
    print(f"Пользователь: {comment['user__username']}, Рейтинг: {comment['rating']}, Текст: {comment['text'][:30]}...")
