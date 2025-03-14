import random
import streamlit as st

# -------------------------------------------------
# 1) Список балів інших студентів (без кандидата)
# -------------------------------------------------
OTHER_SCORES = [
    58.877, 67.033, 63.877, 51.855, 65.655, 46.611, 79.988, 79.488, 59.422, 68.800,
    54.444, 69.688, 71.833, 52.822, 53.511, 58.855, 58.033, 72.277, 69.000, 54.388,
    66.355, 61.555, 90.688, 66.266, 63.333, 62.122, 51.544, 56.377, 62.588, 72.022,
    92.277, 73.200, 50.355, 65.411, 55.855, 61.244, 73.055, 64.755, 62.022, 62.166,
    65.100, 65.788, 79.877, 59.455, 73.766, 52.777, 59.277, 63.066, 59.377, 75.377,
    63.788, 57.644, 58.811, 73.566, 60.711, 53.733, 56.700, 56.677, 62.611, 52.044,
    62.466, 79.077, 58.066, 56.711, 55.744, 69.800, 71.388, 69.088, 77.911, 51.133,
    59.488, 50.666, 77.400, 64.255, 80.933, 65.055, 76.944, 74.888, 54.988, 56.658,
    61.577, 61.255, 70.822, 55.529, 62.755, 71.711, 55.288, 72.011, 62.077, 59.800,
    68.144, 54.011, 73.766, 60.533, 53.344, 79.700, 58.622, 72.366, 87.922, 67.022,
    60.633, 68.622, 74.700, 58.333, 69.600, 71.311, 55.733, 78.500, 70.366, 57.222,
    63.333, 71.155, 68.811, 59.597, 70.766, 73.933, 66.755, 68.355, 59.688, 59.466,
    78.977, 69.811, 67.733, 75.933, 70.144, 61.077, 84.666, 64.677, 78.955, 67.722,
    66.622, 69.511, 54.786, 76.222, 64.044, 65.855, 59.666, 64.622, 72.277, 76.033,
    56.048, 71.488, 71.644, 60.158, 67.077, 74.333, 80.500, 64.011, 74.633, 75.166,
    65.611, 63.500, 74.611, 57.400, 44.166, 78.900, 42.544, 38.633, 64.988, 67.188,
    79.000, 72.466, 71.033, 67.444, 71.755, 62.011, 59.600, 66.411, 61.733, 57.488,
    65.088, 68.600, 70.100, 73.611, 56.422, 78.788, 72.400, 56.633, 59.444, 66.622,
    70.366, 67.788, 72.122, 70.633, 72.688, 70.566, 56.544, 76.122, 61.800, 66.500,
    83.144, 79.811, 37.033, 61.533, 68.877, 71.733, 52.011, 71.455, 74.700, 64.055,
    80.200, 50.455, 64.600, 58.744, 57.022, 59.298, 66.311, 70.144, 70.033, 68.466,
    56.837, 74.955, 84.600, 59.888, 75.700, 55.000, 66.545, 74.333, 62.636, 77.922,
    61.333, 82.011, 81.977, 60.279, 78.822, 55.187, 87.977, 74.855, 68.777, 75.011,
    63.466, 58.013, 61.766, 59.111, 61.216, 53.352, 54.162, 60.055, 74.855, 71.955,
    72.700, 76.800, 63.788, 83.633, 60.186, 75.422, 69.722, 70.500, 69.911, 59.944,
    78.900, 58.066
]

DEPARTMENTS_QUOTA = {
    "СП": 87,
    "СКС": 86,
    "КСМ": 85
}

BASELINE = {
    "СП": 65.0,
    "СКС": 65.0,
    "КСМ": 65.0
}

FIRST_PRIORITY_WEIGHTS = {
    "СП": 60,
    "СКС": 25,
    "КСМ": 15
}

SECOND_PRIORITY_WEIGHTS = {
    "СП": {"СКС": 50, "КСМ": 15},
    "СКС": {"СП": 35, "КСМ": 15},
    "КСМ": {"СП": 35, "СКС": 50}
}


def assign_priorities_for_student():
    first = random.choices(
        population=["СП", "СКС", "КСМ"],
        weights=[FIRST_PRIORITY_WEIGHTS["СП"], FIRST_PRIORITY_WEIGHTS["СКС"], FIRST_PRIORITY_WEIGHTS["КСМ"]],
        k=1
    )[0]
    possible = [dept for dept in ["СП", "СКС", "КСМ"] if dept != first]
    weights = [SECOND_PRIORITY_WEIGHTS[first][dept] for dept in possible]
    second = random.choices(population=possible, weights=weights, k=1)[0]
    third = [dept for dept in ["СП", "СКС", "КСМ"] if dept not in (first, second)][0]
    return [first, second, third]


def simulate_multiround(candidate_score, candidate_priorities):
    students = []
    for s in OTHER_SCORES:
        prios = assign_priorities_for_student()
        students.append({
            "score": s,
            "priorities": prios,
            "candidate": False,
            "admitted": None
        })

    candidate = {
        "score": candidate_score,
        "priorities": candidate_priorities,
        "candidate": True,
        "admitted": None
    }
    students.append(candidate)

    remaining_quota = DEPARTMENTS_QUOTA.copy()

    for round_index in range(3):
        for dept in DEPARTMENTS_QUOTA:
            if remaining_quota[dept] <= 0:
                continue
            applicants = [st for st in students if st["admitted"] is None and st["priorities"][round_index] == dept]
            if not applicants:
                continue
            eligible = [st for st in applicants if st["score"] >= BASELINE[dept]]
            if eligible:
                sorted_applicants = sorted(eligible, key=lambda x: x["score"], reverse=True)
            else:
                sorted_applicants = sorted(applicants, key=lambda x: x["score"], reverse=True)
            admitted_count = 0
            for st in sorted_applicants:
                if admitted_count >= remaining_quota[dept]:
                    break
                st["admitted"] = dept
                admitted_count += 1
            remaining_quota[dept] -= admitted_count

    for st in students:
        if st["candidate"]:
            return st["admitted"]
    return None


def run_simulation_multiround(candidate_score, candidate_priorities, iterations=10000):
    results = {dept: 0 for dept in DEPARTMENTS_QUOTA}
    results["не вступив"] = 0
    for _ in range(iterations):
        result = simulate_multiround(candidate_score, candidate_priorities)
        if result is None:
            results["не вступив"] += 1
        else:
            results[result] += 1
    for k in results:
        results[k] = (results[k] / iterations) * 100
    return results


# STREAMLIT ІНТЕРФЕЙС
def main():
    st.title("🎓 Симуляція мульти-раунд вступу")
    st.write("Оберіть ваші параметри та дізнайтесь, куди з більшою ймовірністю вас зарахують.")

    candidate_score = st.number_input("Ваш конкурсний бал:", min_value=0.0, max_value=100.0, value=75.0, step=0.1)

    candidate_priorities = st.multiselect(
        "Оберіть ваші 3 пріоритети в порядку важливості:",
        options=["СП", "СКС", "КСМ"],
        default=["СП", "СКС", "КСМ"]
    )

    if len(candidate_priorities) != 3 or set(candidate_priorities) != {"СП", "СКС", "КСМ"}:
        st.error("❗ Потрібно вказати рівно 3 унікальні кафедри (СП, СКС, КСМ)!")
        return

    iterations = st.number_input("Кількість симуляцій:", min_value=100, max_value=100000, value=10000, step=100)

    if st.button("🔁 Запустити симуляцію"):
        with st.spinner("Обчислюємо ймовірності..."):
            results = run_simulation_multiround(candidate_score, candidate_priorities, int(iterations))

        st.subheader("📊 Результати симуляції:")
        for dept in ["СП", "СКС", "КСМ", "не вступив"]:
            st.write(f"**{dept}**: {results[dept]:.2f}%")

        st.success("Симуляція завершена!")


if __name__ == "__main__":
    main()
