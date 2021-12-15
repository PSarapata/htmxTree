from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from api.models import Tree
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt


class TreeList(ListView):
    template_name = 'tree/tree_list.html'

    def get_queryset(self):
        return Tree.objects.all()

    def get(self, request):
        trees = self.get_queryset()
        tree_rows = [tree.render_row() for tree in trees]

        return render(request, self.template_name, {'tree_rows': tree_rows, 'title': 'Tree List'})

def expand(request, tree_id):
    tree = Tree.objects.get(id=tree_id)
    child_rows = ""
    level = 0
    if tree.parent_row:
        level = 1
    child_rows = "".join([t.render_row(level, extra={"class": f"collapse_{str(tree.pk)} nested-{level}"}) for t in Tree.objects.filter(parent_row=tree.row.pk)])
    icon = f"""
            <span
                class="collapseicon"
                hx-get="/tree/collapse/{tree.pk}/?level={level}"
                hx-target=".collapse_{str(tree.pk)}"
                hx-swap="outerHTML"
            >
                <i class="far fa-caret-square-up"></i>
            </span>
            """
    return HttpResponse(
        mark_safe(f"""
        <div class="row collapse_{str(tree.pk)} expanded m-{level}" classes="toggle expanded:1s">
            <input type="hidden" name="item" value="{str(tree.pk)}">
            <div class="col">{icon} ({tree.pk}) {tree.row.name}</div>
            <div class="col">{tree.parent_row.pk if tree.parent_row else None}</div>
            <div class="col">{tree.row.pk}</div>
            <div class="col">{tree.lp}</div>
            <form class="sortable active">
            <input type="hidden" name="parent_row" value="{str(tree.parent_row.pk) if tree.parent_row else str(tree.row.pk)}">
            {child_rows}
            </form>
        </div>
        """))

def collapse(request, tree_id):
    level = int(request.GET.get('level', 0))
    tree = Tree.objects.get(id=tree_id)
    return HttpResponse(mark_safe(tree.render_row(level, {"class": "collapsed"})))

@csrf_exempt
def sort_us(request, *args, **kwargs):
    print("input", request.POST.getlist('item'), request.POST.get('parent_row'))
    return HttpResponse("ok")