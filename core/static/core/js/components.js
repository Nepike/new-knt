document.addEventListener("alpine:init", () => {
  // Общее для select и multiSelect: открытие/закрытие, фокус, клавиатура.
  // Только методы и данные — геттеры (active/filtered/...) живут в компонентах,
  // т.к. spread ...base() превратил бы геттер в статичное значение.
  const base = ({ name, options, search = false }) => ({
    open: false, focused: false, query: "", activeIndex: 0, name, options, search,
    toggle() { this.open ? this.close() : this.openMenu(); },
    openMenu() { this.open = true; this.activeIndex = 0; if (this.search) this.$nextTick(() => this.$refs.search.focus()); },
    close() { this.open = false; this.query = ""; },
    onArrow(dir) {
      if (!this.open) { this.openMenu(); return; }
      const n = this.filtered.length;
      if (!n) return;
      this.activeIndex = Math.min(Math.max(this.activeIndex + dir, 0), n - 1);
      this.$nextTick(() => this.$el.querySelector(`[data-opt="${this.activeIndex}"]`)?.scrollIntoView({ block: "nearest" }));
    },
    onEnter() { const o = this.filtered[this.activeIndex]; if (this.open && o) this.pick(o); else this.openMenu(); },
    onFocusOut(e) { if (!this.$el.contains(e.relatedTarget)) { this.focused = false; this.close(); } },
  });

  Alpine.data("select", (cfg) => ({
    ...base(cfg),
    selectedValue: cfg.value ?? null,
    get active() { return this.open || this.focused; },
    get selectedLabel() { const o = this.options.find((o) => o.value === this.selectedValue); return o ? o.label : ""; },
    get filtered() { const q = this.query.trim().toLowerCase(); return q ? this.options.filter((o) => o.label.toLowerCase().includes(q)) : this.options; },
    pick(o) { this.selectedValue = o.value; this.close(); },
    clear() { this.selectedValue = null; },
  }));

  Alpine.data("multiSelect", (cfg) => ({
    ...base(cfg),
    selected: [...(cfg.values ?? [])],
    get active() { return this.open || this.focused; },
    get selectedOptions() { return this.options.filter((o) => this.selected.includes(o.value)); },
    get filtered() { const q = this.query.trim().toLowerCase(); return this.options.filter((o) => !this.selected.includes(o.value) && (!q || o.label.toLowerCase().includes(q))); },
    pick(o) { this.selected.push(o.value); this.query = ""; this.activeIndex = 0; if (this.search) this.$refs.search.focus(); },
    remove(v) { this.selected = this.selected.filter((x) => x !== v); },
  }));
});
