const categoryFilter = document.getElementById("categoryFilter");
const locationFilter = document.getElementById("locationFilter");
const cards = document.querySelectorAll(".ngo-card");

function applyFilters() {
    const selectedCategory = categoryFilter.value;
    const selectedLocation = locationFilter.value;

    let visibleCount = 0;

    cards.forEach(card => {
        const cardCategory = card.getAttribute("data-category");
        const cardLocation = card.getAttribute("data-location");

        const categoryMatch =
            selectedCategory === "" || cardCategory === selectedCategory;

        const locationMatch =
            selectedLocation === "" || cardLocation === selectedLocation;

        if (categoryMatch && locationMatch) {
            card.style.display = "block";
            visibleCount++;
        } else {
            card.style.display = "none";
        }
    });

    // Handle empty state
    const emptyState = document.querySelector(".empty-state");
    if (emptyState) {
        emptyState.style.display = visibleCount === 0 ? "block" : "none";
    }
}

categoryFilter.addEventListener("change", applyFilters);
locationFilter.addEventListener("change", applyFilters);
