from datetime import date

from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Post, Category


def index(request):
    return render(request, 'blog/index.html')


def _shift_month(d, delta):
    """Return the first day of the month `delta` months away from date d."""
    index = d.year * 12 + (d.month - 1) + delta
    return date(index // 12, index % 12 + 1, 1)


def build_dashboard_context():
    """All the numbers the dashboard needs, in one place."""
    today = timezone.localdate()
    this_month = today.replace(day=1)
    last_month = _shift_month(this_month, -1)

    total_posts = Post.objects.count()
    total_categories = Category.objects.count()
    uncategorized = Post.objects.filter(category__isnull=True).count()

    posts_this_month = Post.objects.filter(date_posted__date__gte=this_month).count()
    posts_last_month = Post.objects.filter(
        date_posted__date__gte=last_month,
        date_posted__date__lt=this_month,
    ).count()

    # Percentage change vs last month (None when there is nothing to compare)
    if posts_last_month:
        month_change = round((posts_this_month - posts_last_month) * 100 / posts_last_month)
    else:
        month_change = None

    # Posts per month for the last 6 months (months with 0 posts are included)
    months = [_shift_month(this_month, -i) for i in range(5, -1, -1)]
    counts_by_month = {
        row['month'].date() if hasattr(row['month'], 'date') else row['month']: row['n']
        for row in Post.objects
        .filter(date_posted__date__gte=months[0])
        .annotate(month=TruncMonth('date_posted'))
        .values('month')
        .annotate(n=Count('id'))
    }
    monthly_labels = [m.strftime('%b %Y') for m in months]
    monthly_values = [counts_by_month.get(m, 0) for m in months]

    # Posts per category
    category_stats = list(
        Category.objects.annotate(post_count=Count('posts')).order_by('-post_count', 'name')
    )
    for c in category_stats:
        c.percent = round(c.post_count * 100 / total_posts) if total_posts else 0

    pie_labels = [c.name for c in category_stats if c.post_count]
    pie_values = [c.post_count for c in category_stats if c.post_count]
    if uncategorized:
        pie_labels.append('Uncategorized')
        pie_values.append(uncategorized)

    return {
        'total_posts': total_posts,
        'total_categories': total_categories,
        'uncategorized': uncategorized,
        'posts_this_month': posts_this_month,
        'month_change': month_change,
        'recent_posts': Post.objects.select_related('category').order_by('-date_posted')[:6],
        'category_stats': category_stats[:6],
        'chart_data': {
            'monthly': {'labels': monthly_labels, 'values': monthly_values},
            'categories': {'labels': pie_labels, 'values': pie_values},
        },
    }


def Blog_Dashboard(request):
    """Dashboard page. Also used as the site homepage (see BMIS/views.py)."""
    return render(request, 'blog/dashboard.html', build_dashboard_context())


def Blog_Post_Display(request):
    posts = Post.objects.select_related('category').order_by('-date_posted')
    return render(
        request,
        'blog/blog_post_display.html',
        {'posts': posts})


def Blog_Post_Delete(request, id):
    post = get_object_or_404(Post, id=id)

    post.delete()

    messages.success(request, 'Post deleted successfully.')

    return redirect('Blog_Post_Display')