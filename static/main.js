// AJAX form submission
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#add-item-form");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const name = form.name.value;
    const desc = form.description.value;

    fetch("/api/items/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, description: desc }),
    })
      .then((r) => r.json())
      .then((item) => {
        const list = document.querySelector("#items-list");
        const li = document.createElement("li");
        li.innerHTML =
          `${item.name} – ${item.description} ` +
          `<a href="/delete/${item.id}">Delete</a>`;
        list.appendChild(li);
        form.reset();
      })
      .catch(console.error);
  });
});
