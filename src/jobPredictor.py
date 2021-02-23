import operator

def rank_jobs(G, skills):
    jobs = {}

    for skill in skills:
        # If skill is in knowledge graph
        if skill in G.nodes:
            # Go through all the skill's neighbors and increment their value
            for neighbor in G.neighbors(skill):
                if neighbor not in jobs:
                    jobs[neighbor] = 1
                else:
                    jobs[neighbor] += 1

    # Sort job dictionary by value (number of occurrences)
    sorted_jobs = sorted(jobs.items(), key=operator.itemgetter(1), reverse=True)
    return [job[0] for job in sorted_jobs]
