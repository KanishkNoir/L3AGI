import { useMutation } from '@apollo/client'

import createTeamOfAgentsGql from '../../gql/ai/teamOfAgents/createTeamOfAgents.gql'

export type TeamOfAgentsInput = {
  name: string
  description: string
  team_type: string
}

export const useCreateTeamOfAgentsService = () => {
  const [mutation] = useMutation(createTeamOfAgentsGql)

  const createTeamOfAgentsService = async (input: TeamOfAgentsInput) => {
    const { name, description, team_type } = input

    const {
      data: { createTeamOfAgents },
    } = await mutation({
      variables: {
        input: {
          name,
          description,
          team_type,
        },
      },
    })

    return createTeamOfAgents
  }

  return [createTeamOfAgentsService]
}