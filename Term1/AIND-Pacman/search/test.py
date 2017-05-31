  fringe=util.Stack()
  fringe.push((problem.getStartState(),[],0)) #state, total actions, total cost
    
  state,allactions,allcost=fringe.pop()
  visited_states=[state]
  while (not problem.isGoalState(state)):
      
    successors=problem.getSuccessors(state)
    for next_state,action,cost in successors:
      #print "next state:",next_state, action
      if (not next_state in visited_states):
        fringe.push((next_state,allactions+[action],allcost+cost))
        visited_states.append(next_state)
        #print "visited_states: ",visited_states
    #print "All actions: ",allactions
    state,allactions,allcost=fringe.pop()
    
  return  allactions
