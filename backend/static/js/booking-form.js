document.addEventListener("DOMContentLoaded", () => {
  const toasts = document.querySelectorAll(".toast");

  toasts.forEach((toast, index) => {
    setTimeout(() => {
      toast.classList.add("show");
    }, index * 100);

    setTimeout(() => {
      toast.classList.remove("show");
    }, 3000 + index * 100);
  });
});
