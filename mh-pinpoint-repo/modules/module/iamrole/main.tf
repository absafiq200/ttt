data "aws_iam_policy_document" "assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = var.assume_type
      identifiers = ["${var.trust_role}"]
    }
  }
}

resource "aws_iam_role" "iam_role" {
  name               = var.iam_role_name
  path               = var.iam_role_path
  description        = var.iam_role_description
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "policy" {
  name        = var.iam_policy_name
  description = var.iam_policy_description
  policy      = var.policy
}

resource "aws_iam_role_policy_attachment" "attach_policy" {
  role       = aws_iam_role.iam_role.name
  policy_arn = aws_iam_policy.policy.arn
}