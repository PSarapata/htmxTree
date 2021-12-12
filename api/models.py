from django.db import models
from django.utils.safestring import mark_safe


class SimpleElement(models.Model):
    """
    A simple shell imitating actual element, which has a lot more data.
    """
    name = models.CharField(max_length=100)


class Tree(models.Model):
    """
    Tree model binding SimpleElements together into a tree-like structure.
    """
    parent_row = models.ForeignKey(
        SimpleElement, related_name="tree_rodzic_qs",
        on_delete=models.CASCADE, null=True, blank=True, default=None,
        verbose_name="Element drzewa (rodzic)"
    )
    row = models.ForeignKey(
        SimpleElement, related_name="element_tree_element_qs",
        on_delete=models.CASCADE, null=True, blank=True, default=None,
        verbose_name="Element drzewa (dziecko)"
    )
    lp = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.pk} / parent = {self.parent_row} / lp = {self.lp} / child = {self.row}"

    def przesun_w_gore(self):
        if self.lp > 1:
            try:
                el_tree = Tree.objects.get(parent_row=self.parent_row, lp=self.lp - 1)
                el_tree.lp += 1
                el_tree.save()
            except Tree.DoesNotExist:
                pass
            self.lp -= 1
            self.save()
            return True
        return False

    def przesun_w_dol(self):
        try:
            el_tree = Tree.objects.get(parent_row=self.parent_row, lp=self.lp + 1)
            el_tree.lp -= 1
            el_tree.save()
            self.lp += 1
            self.save()
            return True
        except Tree.DoesNotExist:
            pass
        return False

    def przesun_powiazanie(self, dest_row_id, dest_lp):
        dest_row = Tree.objects.filter(pk=dest_row_id).first()
        node_lp_count = Tree.objects.filter(parent_row=dest_row).count()
        if dest_row:
            dest_row = dest_row.row
        if not dest_lp:
            dest_lp = node_lp_count + 1
        if 1 <= dest_lp <= node_lp_count:
            for newnode_tree in Tree.objects.filter(parent_row=dest_row, lp__gte=dest_lp):
                newnode_tree.lp += 1
                newnode_tree.save()
            for oldnode_tree in Tree.objects.filter(parent_row=self.parent_row, lp__gt=self.lp):
                oldnode_tree.lp -= 1
                oldnode_tree.save()
            self.parent_row = dest_row
            self.lp = dest_lp
            self.save()
            return True
        if dest_lp == node_lp_count + 1:
            for oldnode_tree in Tree.objects.filter(parent_row=self.parent_row, lp__gt=self.lp):
                oldnode_tree.lp -= 1
                oldnode_tree.save()
            self.parent_row = dest_row
            self.lp = dest_lp
            self.save()
            return True
        return False
    
    def render_row(self, level=1):
        expandable = False
        if Tree.objects.filter(parent_row=self.row).count() > 0:
            expandable = True
        icon = f"""
            <span
                hx-get="/tree/expand/{self.pk}/"
                hx-target="#expand_{str(self.pk)}"
                hx-swap="outerHTML"
            >
                <b>></b>
            </span>
            """ if expandable else ""
        indent = "&nbsp;&nbsp;&nbsp;&nbsp;" * level
        return mark_safe(f"""
        <tr id="expand_{str(self.pk)}">
            <td>{indent}{icon} ({self.pk}) {self.row.name}</td>
            <td>{self.parent_row.pk if self.parent_row else None}</td>
            <td>{self.row.pk}</td>
            <td>{self.lp}</td>
        </tr>
        """)

    def to_json(self):
        return {
            "model": self.__class__.__name__,
            "pk": self.pk,
            "fields": {
                "parent_row": self.parent_row.pk if self.parent_row else None,
                "row": self.row.pk,
                "lp": self.lp
            }
        }