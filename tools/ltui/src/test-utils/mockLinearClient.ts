import type { ResolvedConfig } from '../config.js';

interface WorkflowState {
  id: string;
  name: string;
  type: string;
}

interface TeamData {
  id: string;
  key: string;
  name: string;
  description?: string;
  states: WorkflowState[];
}

interface ProjectData {
  id: string;
  name: string;
  slugId: string;
  state: string;
  status: { name: string };
  targetDate: string;
  url: string;
  progress: number;
  issueCountHistory: number[];
  completedIssueCountHistory: number[];
  milestones: Array<{ id: string; name: string; targetDate: string; projectId: string }>;
}

interface LabelData {
  id: string;
  name: string;
  teamId: string;
  color: string;
  isGroup?: boolean;
  parentName?: string;
}

interface UserData {
  id: string;
  name: string;
  email: string;
  displayName: string;
}

interface IssueData {
  id: string;
  identifier: string;
  title: string;
  number: number;
  teamId: string;
  projectId: string;
  stateId: string;
  priority: number;
  assigneeId: string;
  labelIds: string[];
  description: string;
  updatedAt: string;
  createdAt: string;
}

interface DocumentData {
  id: string;
  title: string;
  content: string;
  projectId: string;
  updatedAt: string;
  url: string;
}

interface RoadmapData {
  id: string;
  name: string;
  url: string;
  ownerId: string;
  projectIds: string[];
}

interface MilestoneData {
  id: string;
  name: string;
  projectId: string;
  targetDate: string;
}

interface NotificationData {
  id: string;
  type: string;
  readAt: string | null;
  createdAt: string;
}

const pageInfo = { endCursor: null, startCursor: null };

function connection<T>(nodes: T[]): { nodes: T[]; pageInfo: typeof pageInfo } {
  return { nodes, pageInfo };
}

export function createMockLinearClient(_resolved: ResolvedConfig): any {
  const data = buildData();
  return new MockLinearClient(data);
}

function buildData() {
  const states: WorkflowState[] = [
    { id: 'state-1', name: 'Todo', type: 'backlog' },
    { id: 'state-2', name: 'In Progress', type: 'started' },
  ];
  const teams: TeamData[] = [
    {
      id: 'team-1',
      key: 'ENG',
      name: 'Engineering',
      description: 'Engineering team',
      states,
    },
  ];
  const projects: ProjectData[] = [
    {
      id: 'proj-1',
      name: 'Project Alpha',
      slugId: 'project-alpha',
      state: 'active',
      status: { name: 'On Track' },
      targetDate: '2024-12-31',
      url: 'https://linear.app/project-alpha',
      progress: 0.5,
      issueCountHistory: [10],
      completedIssueCountHistory: [4],
      milestones: [{ id: 'milestone-1', name: 'Milestone 1', targetDate: '2024-10-01', projectId: 'proj-1' }],
    },
  ];
  const labels: LabelData[] = [
    { id: 'label-1', name: 'bug', teamId: 'team-1', color: '#ff0000' },
    { id: 'label-2', name: 'backend', teamId: 'team-1', color: '#00ff00' },
  ];
  const users: UserData[] = [
    { id: 'user-1', name: 'Alice', email: 'alice@example.com', displayName: 'Alice' },
    { id: 'user-2', name: 'Bob', email: 'bob@example.com', displayName: 'Bob' },
  ];
  const issues: IssueData[] = [
    {
      id: 'issue-1',
      identifier: 'ENG-1',
      title: 'Fix bug',
      number: 1,
      teamId: 'team-1',
      projectId: 'proj-1',
      stateId: 'state-1',
      priority: 2,
      assigneeId: 'user-1',
      labelIds: ['label-1'],
      description: 'Issue description',
      updatedAt: '2024-01-02T00:00:00Z',
      createdAt: '2024-01-01T00:00:00Z',
    },
    {
      id: 'issue-2',
      identifier: 'ENG-2',
      title: 'Follow-up',
      number: 2,
      teamId: 'team-1',
      projectId: 'proj-1',
      stateId: 'state-1',
      priority: 1,
      assigneeId: 'user-2',
      labelIds: ['label-2'],
      description: 'Child issue description',
      updatedAt: '2024-01-04T00:00:00Z',
      createdAt: '2024-01-03T00:00:00Z',
    },
  ];
  const documents: DocumentData[] = [
    {
      id: 'doc-1',
      title: 'Design Doc',
      content: 'Document content',
      projectId: 'proj-1',
      updatedAt: '2024-01-05T00:00:00Z',
      url: 'https://linear.app/doc-1',
    },
  ];
  const roadmaps: RoadmapData[] = [
    { id: 'roadmap-1', name: 'Roadmap', url: 'https://linear.app/roadmap', ownerId: 'user-1', projectIds: ['proj-1'] },
  ];
  const milestones: MilestoneData[] = [
    { id: 'milestone-1', name: 'Milestone 1', projectId: 'proj-1', targetDate: '2024-10-01' },
  ];
  const notifications: NotificationData[] = [
    { id: 'notif-1', type: 'issue_created', readAt: null, createdAt: '2024-02-01T00:00:00Z' },
  ];
  return {
    teams,
    states,
    projects,
    labels,
    users,
    issues,
    documents,
    roadmaps,
    milestones,
    notifications,
  };
}

class MockLinearClient {
  private data: ReturnType<typeof buildData>;
  public viewer: any;

  constructor(data: ReturnType<typeof buildData>) {
    this.data = data;
    this.viewer = this.decorateUser(data.users[0]);
  }

  async teams(): Promise<any> {
    return connection(this.data.teams.map(team => this.decorateTeam(team)));
  }

  async team(id: string): Promise<any> {
    const match = this.data.teams.find(team => team.id === id || team.key === id);
    return match ? this.decorateTeam(match) : null;
  }

  async workflowStates(): Promise<any> {
    return connection(this.data.states.map(state => ({ ...state })));
  }

  async workflowState(id: string): Promise<any> {
    return this.decorateState(id);
  }

  async issues(): Promise<any> {
    return connection(this.data.issues.map(issue => this.decorateIssue(issue)));
  }

  async searchIssues(): Promise<any> {
    return connection(this.data.issues.map(issue => ({ id: issue.id })));
  }

  async issue(ref: string): Promise<any> {
    const match = this.data.issues.find(issue => issue.id === ref || issue.identifier === ref);
    return match ? this.decorateIssue(match) : null;
  }

  async createIssue(input: Record<string, unknown>): Promise<any> {
    const created = this.decorateIssue({
      id: 'issue-created',
      identifier: 'ENG-999',
      title: String(input.title ?? 'Generated issue'),
      number: 999,
      teamId: 'team-1',
      projectId: 'proj-1',
      stateId: 'state-1',
      priority: 1,
      assigneeId: 'user-1',
      labelIds: ['label-1'],
      description: String(input.description ?? ''),
      updatedAt: new Date().toISOString(),
      createdAt: new Date().toISOString(),
    });
    return { issue: created };
  }

  async updateIssue(_id: string, _input: Record<string, unknown>): Promise<void> {
    return;
  }

  async createComment(): Promise<any> {
    return {
      comment: {
        id: 'comment-created',
        body: 'comment body',
        createdAt: new Date().toISOString(),
        user: this.decorateUser(this.data.users[0]),
      },
    };
  }

  async createAttachment(): Promise<any> {
    return {
      attachment: {
        id: 'attachment-1',
        title: 'Attachment',
        url: 'https://example.com',
      },
    };
  }

  async createIssueRelation(): Promise<any> {
    return {};
  }

  async projects(): Promise<any> {
    return connection(this.data.projects.map(project => this.decorateProject(project)));
  }

  async project(id: string): Promise<any> {
    const match = this.data.projects.find(project => project.id === id || project.slugId === id);
    return match ? this.decorateProject(match) : null;
  }

  async cycles(): Promise<any> {
    return connection([
      {
        id: 'cycle-1',
        number: 1,
        name: 'Cycle 1',
        startsAt: '2024-01-01',
        endsAt: '2024-01-14',
        status: 'current',
      },
    ]);
  }

  async issueLabels(): Promise<any> {
    return connection(
      this.data.labels.map(label => ({
        ...label,
        parent: label.parentName ? { name: label.parentName } : undefined,
      }))
    );
  }

  async users(): Promise<any> {
    return connection(this.data.users.map(user => this.decorateUser(user)));
  }

  async documents(): Promise<any> {
    return connection(this.data.documents.map(doc => this.decorateDocument(doc)));
  }

  async searchDocuments(): Promise<any> {
    return {
      nodes: this.data.documents.map(doc => this.decorateDocument(doc)),
      pageInfo,
    };
  }

  async document(id: string): Promise<any> {
    const match = this.data.documents.find(doc => doc.id === id);
    return match ? this.decorateDocument(match) : null;
  }

  async roadmaps(): Promise<any> {
    return connection(this.data.roadmaps.map(roadmap => this.decorateRoadmap(roadmap)));
  }

  async roadmap(id: string): Promise<any> {
    const match = this.data.roadmaps.find(roadmap => roadmap.id === id);
    return match ? this.decorateRoadmap(match) : null;
  }

  async projectMilestones(): Promise<any> {
    return connection(this.data.milestones.map(m => this.decorateMilestone(m)));
  }

  async projectMilestone(id: string): Promise<any> {
    const match = this.data.milestones.find(m => m.id === id);
    return match ? this.decorateMilestone(match) : null;
  }

  async notifications(): Promise<any> {
    return connection(
      this.data.notifications.map(n => ({
        ...n,
        createdAt: new Date(n.createdAt),
      }))
    );
  }

  private decorateTeam(team: TeamData) {
    return {
      ...team,
      archivedAt: null,
      states: async () => connection(team.states.map(state => ({ ...state }))),
    };
  }

  private decorateState(stateId: string) {
    const match = this.data.states.find(state => state.id === stateId);
    return match ? { ...match } : undefined;
  }

  private decorateProject(project: ProjectData) {
    const self = this;
    return {
      ...project,
      issueCountHistory: project.issueCountHistory,
      completedIssueCountHistory: project.completedIssueCountHistory,
      teams: async () => connection(self.data.teams.map(team => self.decorateTeam(team))),
      projectMilestones: async () => connection(project.milestones.map(m => self.decorateMilestone(m))),
    };
  }

  private decorateIssue(issue: IssueData) {
    const labels = issue.labelIds
      .map(id => this.data.labels.find(label => label.id === id))
      .filter(Boolean) as LabelData[];
    const team = this.data.teams.find(t => t.id === issue.teamId)!;
    const project = this.data.projects.find(p => p.id === issue.projectId)!;
    const state = this.data.states.find(s => s.id === issue.stateId)!;
    const assignee = this.data.users.find(u => u.id === issue.assigneeId)!;
    return {
      id: issue.id,
      identifier: issue.identifier,
      number: issue.number,
      title: issue.title,
      state,
      team: this.decorateTeam(team),
      project: this.decorateProject(project),
      priority: issue.priority,
      assignee: this.decorateUser(assignee),
      labels,
      description: issue.description,
      createdAt: new Date(issue.createdAt),
      updatedAt: new Date(issue.updatedAt),
      comments: async () =>
        connection([
          {
            id: 'comment-1',
            user: this.decorateUser(this.data.users[1]),
            createdAt: new Date('2024-01-06T00:00:00Z'),
            body: 'Looks good',
          },
        ]),
      history: async () =>
        connection([
          {
            id: 'history-1',
            actor: this.decorateUser(this.data.users[0]),
            createdAt: new Date('2024-01-07T00:00:00Z'),
            toState: this.decorateState('state-2'),
          },
        ]),
    };
  }

  private decorateUser(user: UserData) {
    return { ...user };
  }

  private decorateDocument(doc: DocumentData) {
    const project = this.data.projects.find(p => p.id === doc.projectId)!;
    return {
      ...doc,
      updatedAt: new Date(doc.updatedAt),
      project: this.decorateProject(project),
    };
  }

  private decorateRoadmap(roadmap: RoadmapData) {
    const owner = this.data.users.find(u => u.id === roadmap.ownerId)!;
    return {
      ...roadmap,
      owner: this.decorateUser(owner),
      updatedAt: new Date('2024-01-08T00:00:00Z'),
      projects: async () => connection(roadmap.projectIds.map(id => this.decorateProject(this.data.projects.find(p => p.id === id)!))),
    };
  }

  private decorateMilestone(milestone: MilestoneData) {
    return {
      ...milestone,
      project: this.decorateProject(this.data.projects.find(p => p.id === milestone.projectId)!),
    };
  }
}
