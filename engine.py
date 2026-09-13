from collections import defaultdict

class SkillNetwork:
    def __init__(self):
        # Graph representing who wants what from whom indirectly
        self.graph = defaultdict(list)
        self.user_profiles = {}

    def add_user(self, name, offers, wants):
        self.user_profiles[name] = {"offers": set(offers), "wants": set(wants)}

    def build_network(self):
        """Builds directed edges between users where User A can give what User B wants"""
        self.graph.clear()
        for u1, p1 in self.user_profiles.items():
            for u2, p2 in self.user_profiles.items():
                if u1 == u2:
                    continue
                # If u1 can offer something that u2 wants, create a directed edge u1 -> u2
                mutual_skills = p1["offers"].intersection(p2["wants"])
                if mutual_skills:
                    self.graph[u1].append((u2, list(mutual_skills)))

    def _find_cycles_dfs(self, node, visited, stack, current_path, all_cycles):
        visited.add(node)
        stack.add(node)
        current_path.append(node)

        for neighbor, skills in self.graph[node]:
            if neighbor not in visited:
                self._find_cycles_dfs(neighbor, visited, stack, current_path, all_cycles)
            elif neighbor in stack:
                # Cycle detected! Extract the cyclic path
                cycle_start_idx = current_path.index(neighbor)
                cycle = current_path[cycle_start_idx:]
                # Avoid duplicate permutations of the same loop
                normalized_cycle = tuple(sorted(cycle))
                if normalized_cycle not in all_cycles:
                    all_cycles[normalized_cycle] = cycle

        current_path.pop()
        stack.remove(node)

    def find_optimal_groups(self):
        """Finds all circular learning chains (Groups of 2, 3 or more people)"""
        self.build_network()
        visited = set()
        stack = set()
        all_cycles = {}

        for user in self.user_profiles:
            if user not in visited:
                self._find_cycles_dfs(user, visited, stack, [], all_cycles)

        return list(all_cycles.values())

# --- Tough Simulation Execution ---
if __name__ == "__main__":
    engine = SkillNetwork()

    # Complex circular dependency simulation
    engine.add_user("Anand", offers=["Python"], wants=["React"])
    engine.add_user("Bala", offers=["React"], wants=["Go"])
    engine.add_user("Charlie", offers=["Go"], wants=["Python"])
    engine.add_user("Deepak", offers=["Docker"], wants=["Python"]) # Isolated entry

    print(" Engine analyzing skill dependencies...")
    learning_chains = engine.find_optimal_groups()

    print(f"\n Analysis Complete. Found {len(learning_chains)} optimal multi-way group(s):\n")
    for idx, chain in enumerate(learning_chains, 1):
        chain_str = " -> ".join(chain) + f" -> {chain[0]}"
        print(f"Group #{idx} (Circular Chain): {chain_str}")
        print(" Exchange details:")
        for i in range(len(chain)):
            giver = chain[i]
            receiver = chain[(i + 1) % len(chain)]
            # Get the intersection to show what is being traded
            trade = engine.user_profiles[giver]["offers"].intersection(engine.user_profiles[receiver]["wants"])
            print(f"   - {giver} teaches {list(trade)} to {receiver}")
        print("-" * 50)
