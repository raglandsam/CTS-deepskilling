// 60 & 61. 
const db = db.getSiblingDB('college_nosql');


// 62 & 63. Bulk insert the 10
db.feedback.insertMany([
  {
    "student_id": 1, "course_code": "CS101", "semester": "2022-ODD", "rating": 4,
    "comments": "Excellent teaching. Would recommend.", "tags": ["challenging", "well-structured"],
    "submitted_at": new Date("2022-11-30T10:15:00Z"), "attachments": [{"filename": "notes.pdf", "size_kb": 240}]
  },
  {
    "student_id": 2, "course_code": "CS101", "semester": "2022-ODD", "rating": 5,
    "comments": "Brilliant lab configurations.", "tags": ["practical", "well-structured"],
    "submitted_at": new Date("2022-12-01T14:20:00Z"), "attachments": [{"filename": "labs.pdf", "size_kb": 512}]
  },
  {
    "student_id": 3, "course_code": "CS101", "semester": "2022-ODD", "rating": 2,
    "comments": "Too fast paced.", "tags": ["challenging", "fast-paced"],
    "submitted_at": new Date("2022-12-03T09:00:00Z"), "attachments": []
  },
  {
    "student_id": 4, "course_code": "CS102", "semester": "2022-ODD", "rating": 5,
    "comments": "Deep framework patterns explained clearly.", "tags": ["clear-explanations"],
    "submitted_at": new Date("2022-11-28T11:45:00Z"), "attachments": [{"filename": "patterns.pdf", "size_kb": 1024}]
  },
  {
    "student_id": 5, "course_code": "CS102", "semester": "2022-ODD", "rating": 1,
    "comments": "Disorganized curriculum maps.", "tags": ["disorganized"],
    "submitted_at": new Date("2022-12-05T16:30:00Z"), "attachments": [{"filename": "syllabus.pdf", "size_kb": 120}]
  },
  {
    "student_id": 6, "course_code": "CS103", "semester": "2022-ODD", "rating": 4,
    "comments": "Excellent frontend components walk-through.", "tags": ["practical"],
    "submitted_at": new Date("2022-11-29T13:10:00Z"), "attachments": [{"filename": "ui.pdf", "size_kb": 95}]
  },
  {
    "student_id": 7, "course_code": "CS104", "semester": "2021-EVEN", "rating": 5,
    "comments": "Archived records look good.", "tags": ["legacy"],
    "submitted_at": new Date("2021-05-15T10:00:00Z"), "attachments": [{"filename": "old.zip", "size_kb": 2048}]
  },
  {
    "student_id": 8, "course_code": "CS105", "semester": "2021-EVEN", "rating": 3,
    "comments": "Standard contents overall.", "tags": ["average"],
    "submitted_at": new Date("2021-06-20T12:00:00Z"), "attachments": []
  },
  {
    "student_id": 9, "course_code": "CS103", "semester": "2022-ODD", "rating": 2,
    "comments": "Lacked clear docs.", "tags": ["poor-docs"],
    "submitted_at": new Date("2022-12-02T15:15:00Z"), "attachments": [{"filename": "logs.txt", "size_kb": 40}]
  },
  // 63. Schema-less confirmation document: entirely omit the "attachments" key descriptor
  {
    "student_id": 10, "course_code": "CS102", "semester": "2022-ODD", "rating": 4,
    "comments": "Functional delivery, no file attached.", "tags": ["practical"],
    "submitted_at": new Date("2022-12-06T18:00:00Z")
  }
]);
// 64. Count the active records to verify the baseline count
print("Total Feedback Documents Inserted: " + db.feedback.countDocuments({}));


//TASK 2 : CRUD
//65

db.feedback.find({ "rating": 5 }).forEach(printjson);

//66
db.feedback.find({ "course_code": "CS101", "tags": "challenging" }).forEach(printjson);

//67
db.feedback.find({}, { "student_id": 1, "course_code": 1, "rating": 1, "_id": 0 }).forEach(printjson);

//68
db.feedback.updateMany({ "rating": { "$lt": 3 } }, { "$set": { "needs_review": true } });
db.feedback.find({ "needs_review": true }, { "student_id": 1, "rating": 1, "needs_review": 1, "_id": 0 }).forEach(printjson);

//69
db.feedback.updateMany({ "needs_review": true }, { "$push": { "tags": "reviewed" } });

//70
db.feedback.deleteMany({ "semester": "2021-EVEN" });
//TASK 3 AGGREGATION
// 71 & 72.
print("\n--- Steps 71 & 72: Course Rating Aggregation ---");

var courseStatsPipeline = [
  // Stage 1: $match acts like SQL "WHERE" to filter timeline vectors
  { "$match": { "semester": "2022-ODD" } },
  
  // Stage 2: $group acts like SQL "GROUP BY" to compute server statistics
  { 
    "$group": { 
      "_id": "$course_code", 
      "avg_rating": { "$avg": "$rating" }, 
      "total_feedback_count": { "$sum": 1 } 
    } 
  },
  
  // Stage 3: $project acts like SQL "SELECT" to transform properties and apply mathematical functions
  {
    "$project": {
      "course_code": "$_id",
      "_id": 0,
      "average_rating": { "$round": ["$avg_rating", 1] }, // Rounds to 1 decimal place
      "total_feedback_count": 1
    }
  },
  
  // Stage 4: $sort sorts results (-1 means Descending)
  { "$sort": { "average_rating": -1 } }
];

db.feedback.aggregate(courseStatsPipeline).forEach(printjson);

