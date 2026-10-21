#1 — Implementasi RAW

from dataclasses import dataclass

@dataclass
class Instruction:
    name: str
    destination: str
    sources: list


# Set Instruksi Terpadu (Mendukung pengujian RAW, WAR, dan WAW)
instructions = [
    Instruction("I1", "R1", ["R2", "R3"]),
    Instruction("I2", "R4", ["R5", "R6"]),
    Instruction("I3", "R7", ["R1", "R4"]),
    Instruction("I4", "R2", ["R5", "R8"]),
    Instruction("I5", "R4", ["R7", "R2"]),
    Instruction("I6", "R7", ["R8", "R9"]),
]


# BAGIAN ANGGOTA 1: Fungsi Dependensi RAW
def has_raw_dependency(inst1, inst2):
    """
    RAW (True Data Dependency):
    inst2 membaca register yang sebelumnya ditulis oleh inst1.
    """
    if inst1.destination in inst2.sources:
        return True
    return False


def has_dependency(inst1, inst2):
    return has_raw_dependency(inst1, inst2)


def show_dependencies(instructions):
    print("\n" + "=" * 50)
    print("DEPENDENCY ANALYSIS (RAW)")
    print("=" * 50)
    found = False
    for i in range(len(instructions)):
        for j in range(i + 1, len(instructions)):
            if has_raw_dependency(instructions[i], instructions[j]):
                print(
                    f"{instructions[j].name} depends on {instructions[i].name} "
                    f"[RAW - Register: {instructions[i].destination}]"
                )
                found = True
    if not found:
        print("No dependencies found.")


def sequential_execution(instructions):
    print("\n" + "=" * 50)
    print("SEQUENTIAL EXECUTION")
    print("=" * 50)
    for cycle, inst in enumerate(instructions, start=1):
        print(f"Cycle {cycle}: Executing {inst.name} ({inst.destination} = {' + '.join(inst.sources)})")
    print(f"\nTotal Sequential Cycles: {len(instructions)}")
    return len(instructions)


def parallel_execution(instructions):
    print("\n" + "=" * 50)
    print("INSTRUCTION-LEVEL PARALLEL EXECUTION")
    print("=" * 50)
    completed = set()
    remaining = instructions.copy()
    cycle = 0

    while remaining:
        cycle += 1
        current_cycle = []
        for instruction in remaining:
            dependencies_satisfied = True
            for previous in instructions:
                if previous.name == instruction.name:
                    break
                if has_dependency(previous, instruction) and previous.name not in completed:
                    dependencies_satisfied = False
                    break
            if dependencies_satisfied:
                current_cycle.append(instruction)

        print(f"\nCycle {cycle}:")
        for instruction in current_cycle:
            print(f"  -> {instruction.name}: {instruction.destination} = {' + '.join(instruction.sources)}")
        for instruction in current_cycle:
            completed.add(instruction.name)
            remaining.remove(instruction)

    print(f"\nTotal ILP Cycles: {cycle}")
    return cycle


def main():
    print("\n" + "*" * 60)
    print("      INSTRUCTION-LEVEL PARALLELISM SIMULATOR")
    print("*" * 60)
    print("\nInstruction Set:")
    for inst in instructions:
        print(f"{inst.name}: {inst.destination} = {' + '.join(inst.sources)}")

    show_dependencies(instructions)
    seq_cycles = sequential_execution(instructions)
    ilp_cycles = parallel_execution(instructions)

    speedup = seq_cycles / ilp_cycles
    efficiency = (speedup / len(instructions)) * 100
    print("\n" + "=" * 50)
    print("PERFORMANCE COMPARISON")
    print("=" * 50)
    print(f"Sequential Cycles : {seq_cycles}")
    print(f"ILP Cycles        : {ilp_cycles}")
    print(f"Speedup           : {speedup:.2f}x")
    print(f"ILP Efficiency    : {efficiency:.2f}%")


if __name__ == "__main__":
    main()
