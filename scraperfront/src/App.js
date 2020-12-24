import React, { Component } from 'react';
import "./styles/App.css";
import SearchIcon from '@material-ui/icons/Search';
import CircularProgress from '@material-ui/core/CircularProgress';
import axios from 'axios';

class Navbar extends Component {
  render(){
    return (
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <span className="navbar-brand" style={{marginLeft: 15}}>Medium Scraper</span>
      </nav>
    )
  }
}

class MediumLogo extends React.Component{
  render(){
    return(
      <div className="container pagelogo">
      <img src="https://miro.medium.com/max/8978/1*s986xIGqhfsN8U--09_AdA.png" className="img-fluid" alt="Medium Logo" />
      </div>
    )
  }
}

class JobTable extends Component {
  state = {
    output: null
  }

  handleOutput(jobs){
    // alert(jobs);
    const data= {
      "job_id" : jobs
    }
    axios.post('http://c6a129fe81d8.ngrok.io/scraper/api/crawl/status', data).then(
      res => {
        console.log(res.data.message);
        this.setState({
          output: res.data.message
        })
        var num_of_unfinished_jobs = 0;
        this.state.output.map((item) => {
          if(item === "running" || item === "pending"){
            num_of_unfinished_jobs += 1
          }
        })
        console.log("Number of unfinished jobs = ", num_of_unfinished_jobs)
        if(num_of_unfinished_jobs === 0){
          clearInterval(this.timer);
        }
      }
    )
  }

  componentDidMount(){
    this.timer = setInterval(() => this.updateStatus(), 2000)
  }

  componentWillUnmount(){
    clearInterval(this.timer)
  }

  updateStatus(){
    // console.log("Updating output")
    if(this.props.jobs !== null){
      this.setState({
        output: this.handleOutput(this.props.jobs)
      })
    }
    console.log(this.state.output)
  }

  render(){
    if(this.props.jobs === null || this.state.output === null || this.state.output === undefined){
      return(
        <div></div>
      )
    }
    else{
      return(
        <div>
          <table>
            <thead>
              <tr>
                <th>S. No.</th>
                <th>Blog Title</th>
                {/* <th>Blog Author</th>
                <th>Blog Responses</th> */}
              </tr>
            </thead>
            <tbody>
              {this.state.output.map((item) => 
                  <tr key={this.state.output.indexOf(item)}>
                    <td>{this.state.output.indexOf(item)+1}</td>
                    <td>{item}</td>
                    <td></td>
                    <td></td>
                  </tr>)}
            </tbody>
          </table>
          </div>
      )
    }
  }
}

class CrawlButton extends Component{
  state = {
    message: null,
    unique_id: null,
    status: "",
    jobs: null
  }

  render(){
    return(
      <div className="container">
        <button type="button" className="crawlbutton btn btn-outline-success" onClick={() => {
          this.setState({
            status: "Initializing crawl...."
          })
          let data = {
            tag: this.props.tag
          }
          // alert(this.props.tag)
          axios.post('http://c6a129fe81d8.ngrok.io/scraper/api/crawl/links', data).then(
            res => {
              console.log(res);
              this.setState({
                status: "",
                unique_id: res.data.unique_id,
              })

              let data = {
                unique_id: this.state.unique_id
              }
              axios.post('http://c6a129fe81d8.ngrok.io/scraper/api/crawl/blogs', data).then(
                res => this.setState({
                  jobs: res.data.jobs
                })
              )
            }
          )
        }}>Crawl!!</button><br></br>
        <div className="row">
          <div className="col-lg-5"></div>
        <span className="col-lg-3">{this.state.status}</span></div><br></br>
        <JobTable jobs={this.state.jobs}/>
      </div>
    )
  }
}
class TagInput extends Component{
  state = {
    tag: ""
  }

  render(){
    return(
      <div className="container">
        <div className="container input-group mb-3 taginput">
          <div className="input-group-prepend">
            <span className="input-group-text" id="basic-addon1"><SearchIcon></SearchIcon></span>
          </div>
          <input type="text" className="form-control" placeholder="Enter tag or topic to search blogs!" aria-label="Username" aria-describedby="basic-addon1" onChange={(event) => {
                this.setState({
                  tag: event.target.value
                })
          }}></input>
        </div>
        <CrawlButton tag={this.state.tag}/>
      </div>
    )
  }
}
class App extends Component {
  render() {
    return (
      <div>
        <Navbar />
        <MediumLogo />
        <TagInput />
      </div>
    );
  }
}

export default App;