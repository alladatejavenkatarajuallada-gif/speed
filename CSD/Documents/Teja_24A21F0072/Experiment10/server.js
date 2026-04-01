const express = require("express");
const { graphqlHTTP } = require("express-graphql");
const { buildSchema } = require("graphql");

// 1. GRAPHQL SCHEMA
const schema = buildSchema(`
  type Query {
    welcome: String
    student(id: Int!): Student
  }
  type Mutation {
    addStudent(id: Int!, name: String!, course: String!): Student
  }
  type Student {
    id: Int
    name: String
    course: String
  }
`);
// 2. SAMPLE DATA
const students = [
  { id: 1, name: "John", course: "MERN" },
  { id: 2, name: "Sara", course: "Python" }
]
// 3. RESOLVERS
const root = {
  welcome: () => "Welcome to GraphQL",

  student: ({ id }) => students.find(s => s.id === id),

  addStudent: ({ id, name, course }) => {
    const newStudent = { id, name, course };
    students.push(newStudent);
    return newStudent;
  }
};
// 4. EXPRESS + GRAPHQL SERVER
const app = express();
app.use("/graphql", graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true  // Enables GraphiQL UI
}));
app.listen(4000, () => {
  console.log("🚀 GraphQL server running at http://localhost:4000/graphql");
});