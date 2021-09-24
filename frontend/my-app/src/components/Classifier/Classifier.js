import React, {Component} from 'react';
import Dropzone from 'react-dropzone';
import './Classifier.css'
import {Spinner, Button, Alert, Image, Container, Row, Col} from 'react-bootstrap'
import axios from 'axios'
import image_1 from "../../static_media/1.png"
import image_2 from "../../static_media/2.png"


class Classifier extends Component {
    state = {
        files: [],
        isLoading: false,
        recentImage: null,
    }


    handleClick = (e) => {

        const ImageData = [image_1, image_2]

        const FILES = {
            "image_1": [{
                name: "image_1",
                size: "100",
                image: ImageData[0]
            }],
            "image_2": [{
                name: "image_2",
                size: "200",
                image: ImageData[1]
            }],
            "image_3": [{
                name: "image_3",
                size: "300",
                image: ImageData[1]
            }],
        }

        // you can now use this value to load your images
        const prefix = e.target.dataset.prefix; // 1
        this.setState({
            files: [],
            isLoading: true,
            recentImage: null
        })
        this.loadImage(FILES[`image_${prefix}`])
    }

    onDrop = (files) => {
        this.setState({
            files: [],
            isLoading: true,
            recentImage: null
        })
        this.loadImage(files)
    }

    loadImage = (files) => {
        setTimeout(() => {
            this.setState({
                files,
                isLoading: false
            }, () => {
                console.log(this.state.files[0])
            })
        }, 1000);
    }

    activateSpinner = () => {
        this.setState({
            files: [],
            isLoading: true,
        })
    }

    deactivateSpinner = () => {
        this.setState({isLoading: false})
    }

    sendImage = () => {
        this.activateSpinner()
        let formData = new FormData()
        formData.append('picture', this.state.files[0])
        axios.post('http://127.0.0.1:8000/api/images/', formData, {
            headers: {
                'accept': 'application/json',
                'content-type': 'multipart/form-data'
            }
        })
            .then(resp => {
                this.getImageClass(resp)
                console.log(resp.data.id)
            })
            .catch(err => {
                console.log(err)
            })
    }

    getImageClass = (obj) => {
        axios.get(`http://127.0.0.1:8000/api/images/${obj.data.id}/`, {
            headers: {
                'accept': 'application/json',
            }
        })
            .then(resp => {
                this.setState({recentImage: resp})
                console.log(resp)
            })
            .catch(err => {
                console.log(err)
            })
        this.deactivateSpinner()

    }

    render() {
        const files = this.state.files.map(file => (
            <li key={file.name}>
                {file.name} - {file.size} bytes
            </li>
        ));
        return (

            <Container>

                <Row>
                    <Col>
                        <Dropzone onDrop={this.onDrop} accept='image/png, image/jpeg'>
                            {({isDragActive, getRootProps, getInputProps}) => (
                                <section className="container">
                                    <div {...getRootProps({className: 'dropzone back'})}>
                                        <input {...getInputProps()} />
                                        <i className="far fa-image mb-2 text-muted" style={{fontSize: 100}}></i>
                                        <p className='text-muted'>{isDragActive ? "Drop some images " : "Drag 'n' drop some files here, or click to select files"}</p>
                                    </div>
                                </section>
                            )}
                        </Dropzone>
                    </Col>
                </Row>


                <Row>
                    <Col>
                        <div className="container">
                            <div className="row">
                                <div className="col-sm-4">
                                    <button
                                        data-prefix="1"
                                        onClick={(e) => this.handleClick(e)}
                                        className="btn btn-primary">
                                        Sample 1
                                    </button>
                                </div>
                                <div className="col-sm-4">
                                    <button
                                        data-prefix="2"
                                        onClick={(e) => this.handleClick(e)}
                                        className="btn btn-primary">
                                        Sample 2
                                    </button>
                                </div>
                                <div className="col-sm-4">
                                    <button
                                        data-prefix="3"
                                        onClick={(e) => this.handleClick(e)}
                                        className="btn btn-primary">
                                        Sample 3
                                    </button>
                                </div>
                            </div>
                        </div>
                    </Col>
                </Row>


                <Row>
                    <Col>


                        <div className="mt-2">
                            {
                                this.state.isLoading &&
                                <Spinner animation="border" role="status"></Spinner>
                            }
                        </div>

                        <aside>
                            {files}
                        </aside>

                        <div className="img-fluid">
                            {this.state.files.length > 0 &&
                            <Image
                                src={URL.createObjectURL(this.state.files[0])}
                                height='400' rounded/>
                            }
                        </div>

                        {this.state.recentImage &&
                        <React.Fragment>
                            <Image className='justify-content-center'
                                   src={this.state.recentImage.data.analyzed_picture}
                                   height='400' rounded/>
                        </React.Fragment>
                        }


                    </Col>

                </Row>


                <Row>
                    <Col>
                        {this.state.files.length > 0 &&
                        <Button variant='info' size='lg' className='mt-3' onClick={this.sendImage}>Analyze
                            Image </Button>
                        }

                        {
                            this.state.recentImage &&
                            <div className="mt-2">
                                <Alert variant='primary'>
                                    <p> Time Taken: {this.state.recentImage.data.classified} </p>
                                    <p> Capillary Density: {this.state.recentImage.data.classified} </p>
                                    <p> Number of Capillaries: {this.state.recentImage.data.classified} </p>

                                </Alert>
                            </div>
                        }
                    </Col>

                </Row>


            </Container>


        )
    }
}

export default Classifier;


