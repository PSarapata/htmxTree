from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from api.models import Tree
from django.utils.safestring import mark_safe


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
    level = 1
    child_rows = ""
    indent = ""
    if tree.parent_row:
        parent = Tree.objects.filter(row=tree.parent_row).first()
        level += 1
        while parent:
            parent = Tree.objects.filter(row=parent.parent_row).first()
            level += 1
    child_rows = "".join([t.render_row(level + 1) for t in Tree.objects.filter(parent_row=tree.row.pk)])
    indent = "&nbsp;" * (4 * level)
    icon = f"""
            <span
                hx-get="/tree/collapse/{tree.pk}/?level={level}"
                hx-target="#collapse_{str(tree.pk)}"
                hx-swap="outerHTML"
            >
                <b>v</b>
            </span>
            """
    return HttpResponse(
        mark_safe(f"""
        <tr id="collapse_{str(tree.pk)}">
            <td>{indent}{icon} ({tree.pk}) {tree.row.name}</td>
            <td>{tree.parent_row.pk if tree.parent_row else None}</td>
            <td>{tree.row.pk}</td>
            <td>{tree.lp}</td>
            {child_rows}
        </tr>
        """))

def collapse(request, tree_id):
    level = int(request.GET.get('level', 1))
    tree = Tree.objects.get(id=tree_id)
    return HttpResponse(mark_safe(tree.render_row(level)))