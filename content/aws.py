AWS_DAYS = {
    2: {
        "title": "IAM Users & Least Privilege",
        "phase": "AWS Networking Foundations",
        "status": "topic-verified",
        "summary": "Identity comes before infrastructure: decide who can act, what they can do, and how narrowly that permission can be scoped.",
        "architecture": "Human / workload → IAM principal → policy evaluation → AWS API action",
        "how": [
            "IAM separates identities from permissions. Users, roles and policies let AWS evaluate whether a principal is allowed to perform an action against a resource under the request conditions.",
            "The useful habit is to begin with the smallest permission set that enables the task, then expand only when evidence shows something legitimate is blocked. Broad administrator access is convenient precisely because it skips the design work least privilege requires.",
            "For long-lived workforce access, federation or IAM Identity Center is generally preferable to multiplying permanent IAM-user credentials. The historical lesson here remains the same: identity is an attack surface, so permissions and credentials need deliberate ownership."
        ],
        "commands": "aws sts get-caller-identity\naws iam list-users\naws iam list-roles",
        "verify": "Use aws sts get-caller-identity from the intended session, then test the exact allowed operation and a deliberately disallowed operation. Least privilege is proven by both what works and what is refused.",
        "gotcha": "An IAM policy that looks restrictive can still become broad through wildcards, attached managed policies, role assumption, or resource policies. Read the effective path, not one JSON document in isolation.",
        "security": "Protect root credentials, require MFA where appropriate, avoid embedding access keys in source code, rotate or remove unused credentials, and prefer short-lived role credentials over permanent keys.",
        "lesson": "Cloud security starts with identity. A private subnet does not compensate for an identity that can do everything.",
        "evidence": "Day/topic verified by published project artifact; this blog article is an expanded technical record rather than a claim that every paragraph appeared in the original post."
    },
    4: {
        "title": "Security Groups",
        "phase": "AWS Networking Foundations",
        "status": "topic-verified",
        "summary": "Security Groups control allowed network flows around AWS network interfaces and workloads using stateful rules.",
        "architecture": "Client → Security Group rule evaluation → ENI / workload",
        "how": [
            "A Security Group is a stateful virtual firewall associated with supported resources through their network interfaces. Its rules are allow rules: you describe traffic that is permitted rather than building an ordered firewall ruleset with explicit deny entries.",
            "Stateful matters. When traffic is allowed in one direction, response traffic for that connection is automatically tracked. That is different from a stateless packet filter where both directions must be permitted independently.",
            "Good rules describe intent. Allowing TCP 443 from a load balancer security group is stronger than allowing the same port from the entire internet when only the load balancer should reach the application."
        ],
        "commands": "aws ec2 describe-security-groups\naws ec2 describe-network-interfaces",
        "verify": "Inspect the security groups attached to the workload ENI, confirm the source/destination and port actually match the intended path, then test connectivity from an allowed and a non-allowed source.",
        "gotcha": "Opening the right port on the wrong Security Group changes nothing. Trace which ENI the workload actually uses before editing rules.",
        "security": "Avoid 0.0.0.0/0 or ::/0 for administrative ports unless the design explicitly requires public exposure. Prefer references between security groups for service-to-service paths where possible.",
        "lesson": "A firewall rule is part of an architecture, not a permission-shaped sticky note saying 'make it work'.",
        "evidence": "Day/topic verified by published video evidence. Expanded here as a durable technical explanation."
    },
    11: {
        "title": "VPC Endpoints",
        "phase": "AWS Networking Foundations",
        "status": "topic-verified",
        "summary": "VPC Endpoints let workloads reach supported AWS services without making the public internet the required data path.",
        "architecture": "Private workload → VPC endpoint → supported AWS service",
        "how": [
            "Interface endpoints use AWS PrivateLink and place endpoint network interfaces in selected subnets. Gateway endpoints provide route-table targets for supported services such as Amazon S3 and DynamoDB.",
            "The security benefit is architectural: a private workload can reach a service through an AWS-managed private path instead of depending on an Internet Gateway or NAT path just to call an AWS API.",
            "Endpoint policies, Security Groups on interface endpoints, route tables and DNS all influence whether the path actually works. Creating an endpoint is only one part of the connection."
        ],
        "commands": "aws ec2 describe-vpc-endpoints\naws ec2 describe-route-tables",
        "verify": "Resolve the service name from the workload, inspect endpoint state and route/DNS behavior, then prove the request succeeds without the public egress path the endpoint was meant to replace.",
        "gotcha": "Private DNS on an interface endpoint can change where a familiar public service hostname resolves inside the VPC. DNS is part of the endpoint design, not an afterthought.",
        "security": "Scope endpoint policies and attached Security Groups. A private path is useful, but private does not automatically mean least privilege.",
        "lesson": "Network design improves when private workloads do not need unnecessary public egress just to use cloud-native services.",
        "evidence": "Topic verified through the published Day 12 opener, which explicitly referenced Day 11 VPC Endpoints."
    },
    12: {
        "title": "VPC Peering",
        "phase": "AWS Networking Foundations",
        "status": "topic-verified",
        "summary": "VPC Peering connects two VPCs directly, but routing, addressing and security rules still decide whether applications can communicate.",
        "architecture": "VPC A route table ↔ peering connection ↔ VPC B route table",
        "how": [
            "A peering connection creates a private routing relationship between two VPCs. Both sides need routes for the peer CIDR, and the application path still passes through Security Group and network controls.",
            "Peering is not transitive. If VPC A peers with B and B peers with C, A does not automatically gain a route through B to C. That limitation matters as topologies grow.",
            "Overlapping CIDR ranges prevent the clean routing model peering depends on, so address planning made early can determine whether later connectivity is simple or painful."
        ],
        "commands": "aws ec2 describe-vpc-peering-connections\naws ec2 describe-route-tables",
        "verify": "Confirm the peering state is active, routes exist on both sides, Security Groups permit the application flow, then test the actual service port rather than stopping at ICMP.",
        "gotcha": "A healthy peering object does not create routes for you. 'Peering active' and 'traffic routable' are separate facts.",
        "security": "Route only the CIDRs that need connectivity and keep service-level access scoped with Security Groups rather than treating the peer VPC as automatically trusted.",
        "lesson": "Connectivity is a chain: relationship, routes, policy and application listener all have to agree.",
        "evidence": "Day/topic verified by published video evidence."
    },
    13: {
        "title": "AWS Transit Gateway",
        "phase": "AWS Networking Foundations",
        "status": "topic-verified",
        "summary": "Transit Gateway replaces a growing mesh of point-to-point connections with a hub that can centralize routing between networks.",
        "architecture": "VPC / VPN attachments → Transit Gateway → Transit Gateway route tables → destination attachment",
        "how": [
            "As the number of VPCs grows, full-mesh peering becomes operationally awkward. Transit Gateway provides a regional transit hub to which VPCs and supported network connections can attach.",
            "Transit Gateway route tables can segment which attachments learn and reach which destinations. That lets the routing design express environments such as shared services, production and development without requiring every network to peer directly with every other network.",
            "The hub simplifies topology, but it also becomes important infrastructure. Route propagation, association and the underlying VPC route tables must all be understood when debugging traffic."
        ],
        "commands": "aws ec2 describe-transit-gateways\naws ec2 describe-transit-gateway-attachments\naws ec2 describe-transit-gateway-route-tables",
        "verify": "Trace the source VPC route to the Transit Gateway, the TGW route table decision, the destination attachment and the destination VPC route/security rules.",
        "gotcha": "Centralizing routing does not mean every attachment should share one unrestricted routing domain. A hub can simplify architecture or centralize blast radius depending on how its route tables are designed.",
        "security": "Use separate Transit Gateway route tables and deliberate propagation/association to enforce segmentation, then keep workload-level policy in the destination VPCs.",
        "lesson": "Hub-and-spoke solves topology sprawl only when routing policy stays explicit.",
        "evidence": "Day/topic verified by published video evidence."
    },
    16: {
        "title": "Auto Scaling",
        "phase": "AWS Networking Foundations",
        "status": "topic-verified",
        "summary": "Auto Scaling Groups maintain a desired fleet and can change capacity in response to health and demand instead of treating one server as permanent.",
        "architecture": "Launch Template → Auto Scaling Group → instances across subnets → health / scaling signals",
        "how": [
            "An Auto Scaling Group defines minimum, desired and maximum capacity and launches instances from a launch template. The group continuously tries to keep actual capacity aligned with the desired state.",
            "Scaling policies can adjust capacity from metrics or schedules, while health checks can trigger instance replacement. The design becomes much stronger when instances are disposable and bootstrap themselves from code or images instead of depending on manual configuration.",
            "Scaling the application tier does not automatically scale databases, queues or other shared dependencies. Capacity planning still has to follow the whole request path."
        ],
        "commands": "aws autoscaling describe-auto-scaling-groups\naws autoscaling describe-scaling-activities",
        "verify": "Inspect desired versus in-service capacity, recent scaling activities and health status. For a lab, terminate one managed instance and observe whether the group restores desired capacity.",
        "gotcha": "Auto Scaling can faithfully create more broken instances if the launch template or bootstrap process is broken. Replacement is not repair.",
        "security": "Keep instance roles least-privileged, protect launch-template user data and make replacement instances receive security patches and configuration consistently.",
        "lesson": "Elasticity depends on disposability. A server that requires manual rescue every time it is replaced is not really part of an automated fleet.",
        "evidence": "Day/topic verified by published video evidence."
    },
    19: {
        "title": "AWS Config",
        "phase": "AWS Networking Foundations",
        "status": "topic-verified",
        "summary": "AWS Config records resource configuration state and can evaluate whether resources match defined compliance rules.",
        "architecture": "AWS resources → configuration recorder → configuration history / rules → compliance findings",
        "how": [
            "AWS Config answers a different question from an activity log: what did the configuration of this resource look like, how did it change, and does it currently satisfy a rule?",
            "Managed or custom rules can evaluate properties such as encryption, public exposure or required configuration. The resulting compliance state is useful only when findings have owners and remediation paths.",
            "Configuration history is especially valuable during incident review because it helps connect a current misconfiguration to when the resource state changed."
        ],
        "commands": "aws configservice describe-configuration-recorders\naws configservice describe-compliance-by-config-rule",
        "verify": "Confirm recording is enabled for the intended resource types and region, then inspect a known resource's configuration timeline and rule evaluation result.",
        "gotcha": "AWS Config is not CloudTrail. Config focuses on resource configuration state; CloudTrail records API activity. They answer related but different questions.",
        "security": "Protect the destinations and roles used by Config, choose rules that map to real controls, and avoid treating a green compliance dashboard as proof that an application is secure.",
        "lesson": "Security improves when configuration drift becomes observable instead of discoverable only after an outage or audit.",
        "evidence": "Day/topic verified by published video evidence."
    },
    20: {
        "title": "AWS Systems Manager",
        "phase": "AWS Networking Foundations",
        "status": "topic-verified",
        "summary": "Systems Manager provides managed operational channels for instances and nodes so administration does not have to revolve around exposed SSH access.",
        "architecture": "Operator / automation → Systems Manager service → managed node via agent + IAM",
        "how": [
            "Systems Manager includes capabilities such as Session Manager, Run Command, inventory and patch operations. Managed nodes need the right agent/connectivity and IAM permissions for the feature being used.",
            "Session Manager is useful because it can remove the need to expose an inbound SSH port for routine administration. Access can instead be governed by IAM and recorded through the Systems Manager control plane.",
            "The operational win is consistency: commands and maintenance actions can target managed fleets instead of relying on somebody remembering which host needs a manual login."
        ],
        "commands": "aws ssm describe-instance-information\naws ssm start-session --target INSTANCE_ID",
        "verify": "Confirm the node appears as managed, then open a Session Manager session or run a harmless command and verify the result and audit trail.",
        "gotcha": "Closing port 22 does not magically make Session Manager work. Agent health, network access to SSM endpoints and the instance role all have to be correct.",
        "security": "Scope who can start sessions or run commands, log administrative activity, and avoid giving the managed-node role permissions unrelated to node management.",
        "lesson": "Remote administration is stronger when access is an authenticated control-plane action rather than a permanently exposed network service.",
        "evidence": "Day/topic verified by published video evidence."
    },
    21: {
        "title": "AWS CloudFormation",
        "phase": "AWS Networking Foundations",
        "status": "topic-verified",
        "summary": "CloudFormation turns AWS infrastructure into templates and stacks so desired resources can be reviewed, repeated and changed deliberately.",
        "architecture": "Template → CloudFormation stack → AWS resources → events / outputs / drift",
        "how": [
            "A template declares resources and their relationships. CloudFormation builds a stack from that declaration and tracks the stack as infrastructure changes over time.",
            "Change sets are useful because they show the operations CloudFormation intends to perform before a stack update. Outputs and parameters let templates expose or receive values without hard-coding every environment detail.",
            "Infrastructure as code does not remove risk. It makes the intended change reviewable and repeatable, which is far more useful than a console configuration nobody can reconstruct later."
        ],
        "commands": "aws cloudformation validate-template --template-body file://template.yaml\naws cloudformation describe-stacks\naws cloudformation detect-stack-drift --stack-name STACK_NAME",
        "verify": "Validate the template, inspect stack events after deployment, and compare the created resource properties with the declared template. Use drift detection when manual changes are suspected.",
        "gotcha": "A successful stack does not prove the application works. CloudFormation knows resource state, not whether a real user request succeeds end to end.",
        "security": "Review IAM capabilities, secrets handling and replacement behavior before deployment. Infrastructure code deserves the same code review discipline as application code.",
        "lesson": "The console is useful for inspection; the template should be where repeatable infrastructure intent lives.",
        "evidence": "Day/topic verified by published video evidence."
    },
    22: {
        "title": "AWS CDK",
        "phase": "AWS Networking Foundations",
        "status": "topic-verified",
        "summary": "The AWS CDK lets infrastructure be modeled with programming-language constructs and then synthesized into CloudFormation.",
        "architecture": "CDK app → constructs → cdk synth → CloudFormation template → stack",
        "how": [
            "CDK constructs package infrastructure patterns at different levels of abstraction. The code is not a replacement for CloudFormation underneath; synthesis produces a CloudFormation template that becomes the deployment contract.",
            "Using a programming language gives normal tools such as functions, loops, types and reusable modules, but abstraction can hide important defaults. `cdk diff` is valuable because it brings the generated infrastructure change back into view before deployment.",
            "The durable skill is understanding the AWS resources being generated, not merely learning a fluent API that can produce them."
        ],
        "commands": "cdk synth\ncdk diff\ncdk deploy",
        "verify": "Inspect the synthesized template and diff before deployment, then confirm the resulting CloudFormation stack and resources match the intended design.",
        "gotcha": "High-level constructs can create more resources or permissions than the few lines of CDK code suggest. Review the synthesized output when security or cost boundaries matter.",
        "security": "Treat construct defaults as inputs to review, not automatic best practice. Examine generated IAM policies, network exposure and removal policies.",
        "lesson": "Abstraction is useful when you can still see through it.",
        "evidence": "Day/topic verified by a published frame with the AWS CDK title."
    },
    23: {
        "title": "Terraform Introduction",
        "phase": "AWS Networking Foundations",
        "status": "topic-verified",
        "summary": "Terraform introduces a provider-neutral infrastructure-as-code workflow built around configuration, plans and state.",
        "architecture": "HCL configuration → terraform plan → provider APIs → infrastructure + state",
        "how": [
            "Terraform configuration describes resources and dependencies, providers translate that desired state into API operations, and Terraform state tracks the resource instances it manages.",
            "The workflow matters: initialize providers and backend, inspect a plan, then apply the reviewed change. State is not a disposable cache; it is part of Terraform's model for connecting configuration to real infrastructure.",
            "Remote state with locking and controlled access becomes important when more than one person or automation process can change the same infrastructure."
        ],
        "commands": "terraform init\nterraform fmt -check\nterraform validate\nterraform plan\nterraform apply",
        "verify": "Read the plan before applying it, inspect outputs and provider resources afterward, then run another plan and confirm there is no unexpected drift.",
        "gotcha": "Losing or racing Terraform state can turn an infrastructure change into archaeology. Protect state, lock it where supported, and do not edit it casually.",
        "security": "Keep secrets out of configuration and logs where possible, secure remote state because it can contain sensitive values, and review provider/plugin provenance in controlled environments.",
        "lesson": "Infrastructure as code is not just writing resources in text; it is managing the lifecycle and state of those resources predictably.",
        "evidence": "Day/topic verified by published video evidence."
    },
}

UNVERIFIED_AWS = {
    1: "Published chronology confirmed, exact topic still requires archive evidence.",
    3: "Published chronology confirmed; EC2 is only a historical guess and is not treated as verified.",
    5: "Published chronology confirmed; NACLs are only a historical guess and are not treated as verified.",
    6: "Published chronology confirmed; VPC Fundamentals is only a historical guess and is not treated as verified.",
    7: "Published chronology confirmed; Subnets are only a historical guess and are not treated as verified.",
    8: "Published chronology confirmed; Route Tables are only a historical guess and are not treated as verified.",
    9: "Published chronology confirmed; Internet Gateway is only a historical guess and is not treated as verified.",
    10: "Published chronology confirmed; NAT Gateway is only a historical guess and is not treated as verified.",
    14: "Published chronology confirmed. The old 'Review Day' label was AI-generated and is explicitly unsupported by the canonical ledger.",
    15: "Published chronology confirmed; ELB is only a historical guess and is not treated as verified.",
    17: "Published chronology confirmed; CloudWatch is only a historical guess and is not treated as verified.",
    18: "Published chronology confirmed; CloudTrail is only a historical guess and is not treated as verified.",
}
